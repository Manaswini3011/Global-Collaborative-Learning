# Global Collaborative Learning Platform

A web application designed to connect students from any country, any culture, and any language on one powerful learning platform.

## Features

- **Real-Time Translation**: Text and voice translation for seamless cross-language communication
- **AI-Moderated Teams**: AI guides teams, assigns roles, and keeps everyone productive
- **Smart Recommendations**: AI-powered project ideas based on skills and interests
- **Virtual Discussion Rooms**: Real-time collaboration spaces
- **Progress Dashboards**: Track learning journey and team progress
- **Peer Feedback System**: Give and receive feedback from team members
- **Gamified Rewards**: Earn points, achievements, and level up
- **Resource Sharing**: Share and access learning resources

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python Flask
- **Database**: MySQL (XAMPP)

## Prerequisites

1. **Python 3.7+** installed
2. **XAMPP** installed and running (for MySQL database)
3. **pip** (Python package manager)

## Setup Instructions

### 1. Database Setup

1. Start XAMPP and ensure MySQL is running
2. Open phpMyAdmin (usually at `http://localhost/phpmyadmin`)
3. Import the database schema:
   - Go to phpMyAdmin
   - Click "Import"
   - Select the file `database/schema.sql`
   - Click "Go" to import

Alternatively, you can run the SQL file directly:
```bash
mysql -u root -p < database/schema.sql
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Database Connection

If your MySQL configuration is different from the default, edit `app.py` and update the `DB_CONFIG` dictionary:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Your MySQL password
    'database': 'global_colab',
    'charset': 'utf8mb4'
}
```

### 4. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## Project Structure

```
global-colab/
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── database/
│   └── schema.sql        # Database schema
├── templates/
│   ├── index.html        # Home/login page
│   └── dashboard.html    # Main dashboard
├── static/
│   ├── css/
│   │   ├── style.css     # Main styles
│   │   └── dashboard.css # Dashboard styles
│   └── js/
│       ├── auth.js       # Authentication logic
│       └── dashboard.js  # Dashboard functionality
└── README.md             # This file
```

## Usage

### Registration

1. Navigate to `http://localhost:5000`
2. Click "Register"
3. Fill in your details:
   - Username
   - Email
   - Full Name
   - Password
   - Country (optional)
   - Language preference
   - Skills and interests
4. Click "Create Account"

### Login

1. Enter your email/username and password
2. Click "Login"
3. You'll be redirected to the dashboard

### Dashboard Features

- **Dashboard**: View recommendations, recent activity, and achievements
- **Teams**: Create and manage teams
- **Projects**: Create and track projects
- **Discussions**: Join discussion rooms and chat with team members
- **Progress**: View your learning progress
- **Resources**: Share and access resources

## API Endpoints

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - User login
- `POST /api/logout` - User logout

### User
- `GET /api/user/profile` - Get user profile

### Teams
- `GET /api/teams` - Get user's teams
- `POST /api/teams` - Create new team
- `GET /api/teams/<id>/members` - Get team members

### Projects
- `GET /api/projects` - Get user's projects
- `POST /api/projects` - Create new project

### Recommendations
- `GET /api/recommendations` - Get AI recommendations

### Discussion Rooms
- `GET /api/rooms` - Get discussion rooms
- `POST /api/rooms` - Create discussion room
- `GET /api/rooms/<id>/messages` - Get room messages
- `POST /api/rooms/<id>/messages` - Send message

### Progress
- `GET /api/progress` - Get user progress

### Feedback
- `POST /api/feedback` - Submit peer feedback

### Resources
- `GET /api/resources` - Get resources
- `POST /api/resources` - Upload resource

### Achievements
- `GET /api/achievements` - Get user achievements

## Sample Data

The database schema includes sample users:
- John Doe (USA, English)
- Maria Silva (Brazil, Portuguese)
- Yuki Tanaka (Japan, Japanese)
- Sophie Dupont (France, French)

## Future Enhancements

- Integration with real translation APIs (Google Translate, DeepL)
- Voice translation capabilities
- Advanced AI moderation features
- Real-time notifications
- Video conferencing integration
- Mobile app version

## Translation Features

The platform includes automatic message translation based on user language preferences:

- **Automatic Translation**: Messages are translated to each user's selected language when viewing
- **Language Display**: Shows language indicators (e.g., "EN → ES") for translated messages
- **Original View**: Users can click to view the original message text
- **Current Status**: Uses placeholder translation (see TRANSLATION_SETUP.md for integration guide)

To enable real translation, integrate a translation API (Google Translate, DeepL, etc.) - see `TRANSLATION_SETUP.md` for detailed instructions.

## Notes

- This is a prototype version
- Translation uses placeholder function (see TRANSLATION_SETUP.md for real API integration)
- For production use, implement proper security measures:
  - Use environment variables for sensitive data
  - Implement proper password hashing (bcrypt)
  - Add CSRF protection
  - Use HTTPS
  - Implement rate limiting

## License

This project is a prototype for educational purposes.

## Support

For issues or questions, please check the code comments or create an issue in the repository.

"# Global-Collaborative-Learning" 
