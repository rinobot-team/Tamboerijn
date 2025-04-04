use color_eyre::Result;
use context_attribute::context;
use framework::MainOutput;
use mlua::prelude::*;
use serde::{Deserialize, Serialize};
use types::color::Rgb;
use types::led::Leds;

/*
*   Nodes no Tamboerijn precisam ter os traits Copy, Clone, Debug, Serialize e Deserialize,
*   logo, todos os atributos da struct tambem precisam ter esses traits. Mas o tipo Lua da
*   lib mLua nao tem Copy, e tem o proprio trait Serialize e Deserialize que nao eh o mesmo
*   da lib Serde (eh uma implementacao em cima dele).
*/

// TODO: Conseguir herdar Copy, Serialize, Deserialize
#[derive(Copy, Clone, Debug, Serialize, Deserialize)]
pub struct LuaRunner {
    lua_runtime: Lua,
}

impl Default for LuaRunner {
    fn default() -> Self {
        Self {
            lua_runtime: Lua::new(),
        }
    }
}

#[context]
#[derive(Default)]
pub struct MainOutputs {
    pub some_output: MainOutput<u32>,
}

#[context]
pub struct CreationContext {
    // Nada
}

#[context]
pub struct CycleContext {
    // Nada também
}

impl LuaRunner {
    pub fn new(_context: CreationContext) -> Result<Self> {
        Ok(Self::default())
    }

    pub fn cycle(&mut self, _context: CycleContext) -> Result<MainOutputs> {
        // Logica
        todo!("Nao retorna nada ainda")
    }
}
