use serde::{Deserialize, Serialize};
use serialize_hierarchy::SerializeHierarchy;
use spl_network_messages::{
    GameControllerReturnMessage, GameControllerStateMessage, HulkMessage, VisualRefereeMessage,
};

#[derive(Clone, Debug, Deserialize, Serialize, SerializeHierarchy)]
pub enum IncomingMessage {
    GameController(GameControllerStateMessage),
    Spl(HulkMessage),
}

impl Default for IncomingMessage {
    fn default() -> Self {
        Self::Spl(Default::default())
    }
}

#[derive(Clone, Debug, Deserialize, Serialize, SerializeHierarchy)]
pub enum OutgoingMessage {
    GameController(GameControllerReturnMessage),
    Spl(HulkMessage),
    VisualReferee(VisualRefereeMessage),
}

impl Default for OutgoingMessage {
    fn default() -> Self {
        Self::Spl(Default::default())
    }
}
