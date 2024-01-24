<h3 align="center">financial-asset-monitor</h3>

  <p align="center">
    Visually track any financial asset on a Raspberry-Pi Zero W (2) and a supported display.
    <br />
    <a href="https://github.com/TomMcKenna1/financial-asset-monitor/issues">Report Bug</a>
    ·
    <a href="https://github.com/TomMcKenna1/financial-asset-monitor/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#configuration">Configuration</a></li>
    <li><a href="#examples">Examples</a></li>
    <li><a href="#adding-an-unsupported-display">Adding an unsupported display</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

![](https://github.com/TomMcKenna1/financial-asset-monitor/blob/main/resources/demo.png)

Easily monitor any financial asset using a Raspberry-Pi Zero W (2) and an e-ink display. This project supports any financial asset available on Yahoo Finance, and can be configured to display a single asset, or multiple assets at the same time.

**Key features**:
 - Monitor any single or multiple asset(s) available on Yahoo Finance
 - Set a refresh delay to check for price updates
 - Show a line or candlestick chart
 - Screen safe feature to fully refresh an e-ink display every 24 hours
 - Easily configurable via config.yml file
 - Easily add a screen implementation if your display is currently unsupported

<!-- GETTING STARTED -->
## Getting Started

To run this project, follow the steps below.

### Raspberry Pi setup
The first step is to setup your raspberry pi and install the necessary dependancies. Please follow the below steps:

1. Flash your rasberry-pi with the latest stable Raspberry Pi OS Lite. You must configure the image with your WiFi details, and enable SSH.
2. SSH into your raspberry-pi
3. Enable the SPI interface by running the command:
    ```sh
    sudo raspi-config
    ```
    This will launch the raspi-config utility. Enter “Interfacing Options”. Highlight the “SPI” option and toggle it on.
3. Install the necessary dependancies:
    ```sh
    sudo apt update
    sudo apt install git-all python3-pip python3-dev python3-pandas python3-pil python3-numpy
    ```

### For Waveshare displays
In order to use waveshare e-ink displays, you must install the necessary drivers. To do this, please follow the steps below:

1. Clone the driver repository:
  ```sh
  git clone https://github.com/waveshareteam/e-Paper ~/e-Paper
  ```
2. Install the necessary drivers:
  ```sh
  pip3 install ~/e-Paper/RaspberryPi_JetsonNano/python/
  ```

### Running the project
To run the project, clone the repository and run the `main.py` file. All configuration is handled within the `config.yml` file. Please see <a href="#examples">Examples</a> for configuration examples.

1. Clone the repository:
  ```sh
  git clone https://github.com/TomMcKenna1/financial-asset-monitor
  ```
2. Install project dependancies:
   ```sh
   cd financial-asset-monitor
   pip3 install -r requirements.txt
   ```
3. Run the `main.py` file:
  ```sh
  python3 main.py
  ```

<!-- CONFIG EXAMPLES -->
## Configuration

The following configuration options are currently supported:

 * **display** - Contains all options regarding the display used:
   - **id**: `str` - The ID of the display (*REQUIRED*)
   - **flipped**: `bool` - The orientation of the screen (*OPTIONAL*)
 * **assets** - Contains all options regarding the assets displayed:
   - **ticker**: `str` - The ticker of the asset as seen on Yahoo Finance (*REQUIRED*)
   - **name**: `str` - The name of the asset (*OPTIONAL*)
 * **chart** - Contains all options regarding the charts displayed:
   - **candles**: `bool` - Enable or disable candle sticks (*OPTIONAL*)
   - **font**: `str` - The path of the font used (*OPTIONAL*)
   - **font_variant**: `str` - The font variant (*OPTIONAL*)
   - **font_size**: `int` - The size of the font (*OPTIONAL*)
 * **refresh_delay**: `int` - The number of seconds between refreshing assets (REQUIRED)
 * **screen_safe_interval**: `int` - The number of seconds between full refreshing the screen. This option is useful when dealing with e-ink displays that require full refreshingevery so often. (OPTIONAL)

## Examples

### BTC with candle stick chart
![](https://github.com/TomMcKenna1/financial-asset-monitor/blob/main/resources/btc_demo.png)

Display Bitcoin/USD fullscreen with a candle chart:

```yaml
display:
  id: "waveshare_3in52" # Enter your display implementation

assets:
  - ticker: "BTC-USD"
    name: "BTC"

chart:
  candles: true
  font_size: 30

refresh_delay: 180

screen_safe_interval: 86400 # 24 hours
```

### META, AAPL, AMZN, GOOG with line charts
![](https://github.com/TomMcKenna1/financial-asset-monitor/blob/main/resources/four_asset_demo.png)

Display Meta, Apple, Amazon and Google stocks each with their respective line chart:

```yaml
display:
  id: "waveshare_3in52" # Enter your display implementation

assets:
  - ticker: "META"
  - ticker: "AAPL"
  - ticker: "AMZN"
  - ticker: "GOOG"

chart:
  font_size: 30

refresh_delay: 180

screen_safe_interval: 86400 # 24 hours
```

## Adding an unsupported display
If your display is currently not supported, it is relatively easy to add a display implementation to the asset tracker.

Please follow the steps below:
1. Navigate to the displays directory within the asset tracker:
   ```sh
   cd asset_tracker/displays
   ```
2. Create a new python file under whatever name you want:
   ```sh
   touch YOUR-NAME-HERE.py
   ```
3. Within this python file, import both the base Display and the DisplayFactory classes:
   ```python
   from .base import Display
   from .display_factory import DisplayFactory
   ```
4. In the same python file, create a class that inherits from the Display class. You must decorate this class with the DisplayFactory.register method:
   ```python
   @DisplayFactory.register("YOUR-DISPLAY-ID")
   class YOUR-DISPLAY(Display):
       pass
   ```
5. This class must contain all function implementations defined in the base Display class.

<!-- ROADMAP -->
## Roadmap

- [ ] Support different time series (currently only supports monthly)

See the [open issues](https://github.com/TomMcKenna1/financial-asset-monitor/issues) for a full list of proposed features (and known issues).

<!-- CONTRIBUTING -->
## Contributing

Any contributions you make are **greatly appreciated**; I try to promptly check all of them!

If you have a suggestion that would improve this project, please fork the repo and create a pull request. You can also simply open an issue with the label "enhancement".
Don't forget to give the project a star! Thanks again.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<!-- CONTACT -->
## Contact

Tom McKenna - [Follow me on LinkedIn!](https://www.linkedin.com/in/tom-m-8a70891a8/) - tom2mckenna@gmail.com

Project Link: [https://github.com/TomMcKenna1/financial-asset-monitor](https://github.com/TomMcKenna1/financial-asset-monitor)
