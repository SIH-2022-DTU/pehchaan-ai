# pehchaan-ai
 
### Installation

1. Make sure local mongodb is running. 

2. Clone the repo
   ```
   $ git clone https://github.com/SIH-2022-DTU/pehchaan-ai.git
   $ cd pehchaan-ai
   ```
2. Activating virtual environment (optional)
   ```
   $ python -m venv venv
   $ venv\Scripts\activate (for windows)
   $ venv\bin\activate (for mac)
   ```
3. Install requirements
   ```
   $ pip install -r requirements.txt
   ```
4. Run Application

   ```
   $ uvicorn index:app --reload
   ```
5. Open browser and go to the below link. Check out the docs to test the APIs as well.

    ```
    $ http://localhost:8000/docs
    ```