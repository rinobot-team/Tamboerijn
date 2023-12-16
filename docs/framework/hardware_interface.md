# Hardware Interface

TODO: Elaborate

- Hardware Interface
    - Trait
        - `produce_sensor_data()`
    - NAO
        - HardwareId retrieval (from HULA)
        - LoLA/HAL/HULA
            - Explain abbreviations
            - Overview: State/Connection/Network/Component Diagram, DataFlow Model
            - Socket Location and that it is a Unix Socket
            - Proxy
                - Message extraction and injection
                - Message format
                - LED animations
            - Aliveness
                - Network: Message format, UDP, multicast, JSON
                - Service states
            - `produce_sensor_data()`
        - Cameras
            - Video4Linux
            - Buffering, Zero-copy (-> Cycler)
            - Camera setup (registers)
        - Audio
            - ALSA
            - ALSA configuration
            - Later: Audio playback, Text-to-speech
    - Webots
        - HardwareId retrieval (robot name)
        - Webots bindings
        - `produce_sensor_data()`
        - Image, audio transfer to different threads
        - Simulation World
        - Directory structure, symlink
