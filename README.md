# URL Shortener API

The URL Shortener API is a service that allows users to create shortened URLs, manage created URLs, and add additional features such as user authentication and URL limitations.

## ✨ Features

- 🔗 **Generate short URLs** from long URLs
- 🧑‍💻 **User authentication** using JWT
- 📜 **List of created URLs** by users
- 📊 **Hit counter** for tracking URL visits
- ⏳ **Expiration date** for shortened URLs
- 🔠 **Custom short URLs** (slug)
- 🗑️ **Automatic deletion of expired URLs**

---

## 🚀 Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/aldi-rahmaddani/py-url-shortener.git
cd py-url-shortener
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate  # For Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file in the project root and add:

```env
DATABASE_URL=mysql+mysqlconnector://username:password@host/database_name
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5️⃣ Run the Server

```bash
uvicorn main:app --reload
```

The application will be available at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📡 API Endpoints

### 1️⃣ **Authentication**

- **POST** `/register` → Register a new user
- **POST** `/login` → Obtain an access token

### 2️⃣ **URL Management**

- **POST** `/shorten` → Create a shortened URL
- **GET** `/urls` → Retrieve the user's URL list
- **GET** `/{short_code}` → Redirect to the original URL
- **DELETE** `/urls/{id}` → Delete a URL

### 3️⃣ **Admin & Maintenance**

- **POST** `/run-cleanup` → Remove expired URLs

Full API documentation is available in **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) or ini **Redoc** : [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🎯 Deployment

This project can be deployed on **Railway**. Steps:

1. Push the code to GitHub
2. Connect the repository to Railway
3. Add environment variables as defined in `.env`
4. Deploy and run the application

---

## 🤝 Contribution

If you want to contribute:

1. Fork this repository
2. Create a new branch (`git checkout -b new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin new-feature`)
5. Create a Pull Request

---

## 📜 License

MIT License © Aldi Rahmaddani
