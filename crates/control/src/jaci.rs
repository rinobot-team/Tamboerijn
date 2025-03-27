/*
Por enquanto to usando o nome Jaci que o Guadalupe recomendou se não me engano.

Esse código, obviamente, ainda está em desevolvimento

To utilizando como base o Node ./sole_pressure_filter.rs e o exemplo da documentação.
*/
use color_eyre::Result;
use context_attribute::context;
use framework::MainOutput;
use mlua::prelude::*;
use mlua::serde;
use serde::{Deserialize, Serialize}; // Não sei pq ta tando erro de import aqui!
use types::color::Rgb;
use types::led::Leds;

// Estrutura principal de Jaci, responsável por gerenciar o runtime Lua
#[derive(Serialize, Deserialize)]
pub struct Jaci {
    lua_runtime: Lua, 
}

// Essas structs são basicas na criação de um Node
#[context]
pub struct CreationContext {}

#[context]
pub struct CycleContext {}

#[context]
#[derive(Default)]
pub struct MainOutputs {
    pub res: MainOutput<bool>,
}

impl Jaci {
    // Cria uma nova instância de Jaci com um runtime Lua
    pub fn new(_context: CreationContext) -> Result<Self> {
        Ok(Self {
            lua_runtime: Lua::new(),
        })
    }

    // Executa o ciclo principal, incluindo a função de mudança de cor
    pub fn cycle(&mut self, context: CycleContext) -> Result<MainOutputs> {
        self.lua_runtime
            .create_function(|lua_runtime, (r, g, b): (u8, u8, u8)| {
                change_left_eye_color(lua_runtime, (r, g, b))
            })?;

        Ok(MainOutputs {
            res: framework::MainOutput { value: true }.into(),
        })
    }
}

// Função teste para alterar a cor do olho esquerdo
fn change_left_eye_color(_: &Lua, (r, g, b): (u8, u8, u8)) -> LuaResult<bool> {
    let _led_colour = Rgb { r, g, b };
    Ok(true)
}

// TODO: Executar qualquer codigo lua
