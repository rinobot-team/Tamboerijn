use bincode::deserialize;
use futures_util::{stream::SplitStream, StreamExt};
use log::{debug, error, info};
use serde_json::from_str;
use tokio::{net::TcpStream, sync::mpsc::Sender};
use tokio_tungstenite::{tungstenite, MaybeTlsStream, WebSocketStream};

use crate::{
    client::{
        connector, parameter_subscription_manager,
        responder::{Message, Response},
    },
    messages::{
        BinaryOutputsResponse, BinaryResponse, ParametersResponse, TextualOutputsResponse,
        TextualResponse,
    },
};

use super::{output_subscription_manager, responder};

pub async fn receiver(
    mut reader: SplitStream<WebSocketStream<MaybeTlsStream<TcpStream>>>,
    responder: Sender<Message>,
    output_subscription_manager: Sender<output_subscription_manager::Message>,
    parameter_subscription_manager: Sender<parameter_subscription_manager::Message>,
    connector: Sender<connector::Message>,
) {
    while let Some(message) = reader.next().await {
        debug!("Receiver got message: {message:?}");
        match message {
            Ok(message) => match message {
                tungstenite::Message::Text(content) => {
                    let message = match from_str::<TextualResponse>(&content) {
                        Ok(payload) => payload,
                        Err(error) => {
                            error!("Failed to deserialize message content: {error:?}\nMessage was {content:#?}");
                            continue;
                        }
                    };
                    match message {
                        TextualResponse::Outputs(outputs_message) => match outputs_message {
                            TextualOutputsResponse::GetFields { id, fields } => {
                                respond(&responder, id, Response::Fields(fields)).await
                            }
                            TextualOutputsResponse::GetNext { id: _, result: _ } => todo!(),
                            TextualOutputsResponse::Subscribe { id, result } => {
                                respond(&responder, id, Response::Subscribe(result)).await
                            }
                            TextualOutputsResponse::Unsubscribe { id, result } => {
                                respond(&responder, id, Response::Unsubscribe(result)).await
                            }
                            TextualOutputsResponse::SubscribedData { items } => {
                                if let Err(error) = output_subscription_manager
                                    .send(output_subscription_manager::Message::Update { items })
                                    .await
                                {
                                    error!("{error}");
                                }
                            }
                        },
                        TextualResponse::Parameters(parameters_message) => match parameters_message
                        {
                            ParametersResponse::GetFields { id, fields } => {
                                respond(&responder, id, Response::ParameterFields(fields)).await
                            }
                            ParametersResponse::Subscribe { id, result } => {
                                respond(&responder, id, Response::Subscribe(result)).await
                            }
                            ParametersResponse::Unsubscribe { id, result } => {
                                respond(&responder, id, Response::Unsubscribe(result)).await
                            }
                            ParametersResponse::SubscribedData {
                                subscription_id,
                                data,
                            } => {
                                if let Err(error) = parameter_subscription_manager
                                    .send(parameter_subscription_manager::Message::Update {
                                        subscription_id,
                                        data,
                                    })
                                    .await
                                {
                                    error!("{error}");
                                }
                            }
                            ParametersResponse::Update { id, result } => {
                                respond(&responder, id, Response::Update(result)).await
                            }
                            ParametersResponse::GetCurrent { id: _, result: _ } => todo!(),
                            ParametersResponse::LoadFromDisk { id: _, result: _ } => todo!(),
                            ParametersResponse::StoreToDisk { id: _, result: _ } => todo!(),
                        },
                        message => todo!("unimplemented message {message:?}"),
                    }
                }
                tungstenite::Message::Close(close_frame) => {
                    info!("closed: {close_frame:?}");
                    break;
                }
                tungstenite::Message::Binary(data) => {
                    let response = match deserialize::<BinaryResponse>(&data) {
                        Ok(payload) => payload,
                        Err(error) => {
                            error!("Failed to deserialize binary message content: {error:?}");
                            continue;
                        }
                    };
                    let message = match response {
                        BinaryResponse::Outputs(binary_output_response) => {
                            match binary_output_response {
                                BinaryOutputsResponse::GetNext {
                                    reference_id: _,
                                    data: _,
                                } => todo!(),
                                BinaryOutputsResponse::SubscribedData { referenced_items } => {
                                    output_subscription_manager::Message::UpdateBinary {
                                        referenced_items,
                                    }
                                }
                            }
                        }
                    };
                    output_subscription_manager.send(message).await.unwrap();
                }
                _ => {
                    error!("Got unsupported message type from socket");
                    break;
                }
            },
            Err(error) => {
                error!("Error while receiving message from socket: {error:?}");
                output_subscription_manager
                    .send(output_subscription_manager::Message::Disconnect)
                    .await
                    .unwrap();
                connector
                    .send(connector::Message::ConnectionFailed {
                        info: "Peer disconnected".to_string(),
                    })
                    .await
                    .unwrap();
            }
        }
    }
}

async fn respond(responder: &Sender<responder::Message>, id: usize, response: responder::Response) {
    if let Err(error) = responder.send(Message::Respond { id, response }).await {
        error!("{error}");
    }
}
