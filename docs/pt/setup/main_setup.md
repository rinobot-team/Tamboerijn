# Setup Principal e Compilação para o WeBots

Essa seção vai te guiar pela instalação das dependencias e compilação do código para o [WeBots](https://cyberbotics.com/#download)

É recomendado utilizar [Ubuntu 23.10](https://releases.ubuntu.com/mantic/) ou outra distribuição de Linux.

## Instalando Dependências

É necessário instalar alguns pacotes antes de compilar e rodar o código.
Use o package manager da sua distribuição para instalar as seguintes dependencias:

=== "Arch Linux/Manjaro"

    1. Instalar dependencias

        ```sh
        yay -S git git-lfs base-devel rustup rsync cmake clang hdf5 opusfile python webots
        ```
        `yay` é preciso porque `webots` é um pacote [AUR](https://aur.archlinux.org/).
        Outro cliente AUR pode ser utilizado.

    1. Instalar a toolchain do rust

        ```sh
        rustup default stable
        ```

=== "Ubuntu"

    1. Instalar dependencias

        ```sh
        sudo apt install git git-lfs build-essential libssl-dev pkg-config libclang-dev rsync cmake libhdf5-dev libopusfile-dev python3 libasound2-dev libluajit-5.1-dev libudev-dev
        ```

    1. Instalar Webots
        Baixe o WeBots de [https://cyberbotics.com/](https://cyberbotics.com/), baixará um arquivo XXXX.deb para ser instalado.

        ```sh
        sudo dpkg -i XXXX.deb
        ```

    1. Instalar a toolchain do rust

        Visite [https://rustup.rs/](https://rustup.rs/) para um tutorial atualizado.

        ln -s ~/tools/webots/webots ~/.local/bin/webots
        ```

    1. Install rust toolchain

        Visit [https://rustup.rs/](https://rustup.rs/) for up to date instructions.

## Adquirindo o código

Clone o repositório do github [rinobot-team/Tamboerijn](https://github.com/rinobot-team/Tamboerijn) :

```sh
git clone git@github.com:rinobot-team/Tamboerijn.git
```

*Se houver algum problema com o ssh contacte a gerência*

## Compilando para Webots

No root do repositório há um script chamado `pepsi`. Veja [pepsi](../tooling/pepsi.md) para mais detalhes. 
Execute o comando no root do repostiório para compilar o binário usado pelo WeBots.
Isso irá compilar o pepsi, e depois o código em si, então deve demorar um pouco.

```sh
./pepsi build
```

## Rodando o WeBots

Com o passo da compilação completo, abre o WeBots e carregue a cena localizada em `webots/worlds/penalized.wbt`.

## Rodar o Webots em External Mode

Para que não precise recarregar a cena toda vez que compilar o código, é possível rodar `webots/worlds/penalized_extern.wbt` e ligar o controller com:

```sh
./pepsi run
```

## Executando o simulator de comportamento

Para que possa rodar diferentes arquivos de comportamento no simulador é preciso que tenha o pacote ```inspect``` de lua instalado. Pode ser baixado e salvo no path do lua ou baixado usando o package manager do lua.

Depois você pode rodar o simulador executando este comando no root do repositório:
```sh
cargo run --manifest-path=tools/behavior_simulator/Cargo.toml serve tests/behavior/golden_goal.lua
```
O resultado pode ser visto utilizando o `twix`.
