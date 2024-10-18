# Yandex maps company info parser
Parser parses company information(photos, reviews, name)

## Installation
1. Clone project
    ```shell
    # https
    git clone https://github.com/SaD-Pr0gEr/yandex_company_info_parser.git
    
    # ssh
    git clone git@github.com:SaD-Pr0gEr/yandex_company_info_parser.git
    ```
2. Create virtual env and Install requirements
    ```shell
    cd yandex_company_info_parser

    python3 -m venv env

    # unix
    source env/bin/activate

    # windows
    env\Scripts\activate

    pip install -r requirements.txt
    ```
3. Install external tools
    * You need to install chrome(you can change to firefox or any other browser in code)
    * Download [chromedriver](https://googlechromelabs.github.io/chrome-for-testing/)
    * Store chromedriver in drivers folder($project_root_path/drivers)
4. Set maps links
    * In `main.py` you can define maps urls
5. Run code
    Run project with command `python main.py`
