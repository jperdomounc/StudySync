# StudySync - Angular + Spring Boot Edition
**UNC Class & Professor Rating System**

This is the rewritten version of StudySync using **Angular 17+** (TypeScript) and **Spring Boot 3.x** (Java 17).

## Architecture

### Backend: Spring Boot 3.x
- **Framework**: Spring Boot with Spring Security
- **Database**: MongoDB with Spring Data MongoDB
- **Authentication**: JWT tokens with BCrypt password hashing
- **Build Tool**: Maven
- **Java Version**: 17+

### Frontend: Angular 17+
- **Framework**: Angular 17+ with TypeScript
- **Architecture**: Standalone Components
- **State Management**: RxJS with Services
- **HTTP**: Angular HttpClient with Interceptors
- **Routing**: Angular Router with Auth Guards

## Features

### Authentication System
- UNC email validation (@unc.edu, @live.unc.edu, @ad.unc.edu)
- Secure JWT token-based authentication
- BCrypt password hashing
- Auth guard for protected routes

### Class & Professor Rating
- Rate class difficulty (1-10 scale)
- Rate professors (1-5 stars with reviews)
- Browse by major
- View rankings and statistics

## Project Structure

```
ScheduleMaker/
├── spring-backend/              # Spring Boot backend
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/studysync/
│   │   │   │   ├── config/      # Security & app configuration
│   │   │   │   ├── controller/  # REST controllers
│   │   │   │   ├── dto/         # Data Transfer Objects
│   │   │   │   ├── model/       # MongoDB entities
│   │   │   │   ├── repository/  # MongoDB repositories
│   │   │   │   ├── security/    # JWT utilities
│   │   │   │   ├── service/     # Business logic
│   │   │   │   └── StudySyncApplication.java
│   │   │   └── resources/
│   │   │       └── application.yml
│   │   └── test/
│   ├── pom.xml
│   └── Dockerfile
│
└── angular-frontend/            # Angular frontend
    ├── src/
    │   ├── app/
    │   │   ├── components/      # UI components
    │   │   ├── services/        # API & state services
    │   │   ├── models/          # TypeScript interfaces
    │   │   ├── guards/          # Route guards
    │   │   ├── interceptors/    # HTTP interceptors
    │   │   ├── app.component.ts
    │   │   ├── app.routes.ts
    │   │   └── app.config.ts
    │   ├── environments/        # Environment configs
    │   ├── index.html
    │   ├── main.ts
    │   └── styles.css
    ├── angular.json
    ├── package.json
    ├── tsconfig.json
    ├── Dockerfile
    └── nginx.conf
```

## Prerequisites

### For Local Development
- **Java 17+** (OpenJDK or Oracle JDK)
- **Maven 3.8+**
- **Node.js 18+** and npm
- **Angular CLI 17+**: `npm install -g @angular/cli`
- **MongoDB 7.0+** (via Docker or local installation)
- **Git**

### For Docker Deployment
- **Docker** 20.10+
- **Docker Compose** 2.0+

## Getting Started

### Option 1: Local Development

#### 1. Start MongoDB

Using Docker:
```bash
docker run -d \
  --name studysync-mongodb \
  -p 27017:27017 \
  -e MONGO_INITDB_DATABASE=studysync \
  mongo:7.0
```

Or use existing docker-compose:
```bash
docker-compose up -d mongodb
```

#### 2. Backend Setup (Spring Boot)

```bash
# Navigate to backend directory
cd spring-backend

# Copy environment file
cp .env.example .env
# Edit .env and set your JWT_SECRET_KEY

# Build and run
./mvnw spring-boot:run

# Or build JAR and run
./mvnw clean package
java -jar target/studysync-backend-2.0.0.jar
```

Backend will start at: **http://localhost:8080**

API endpoints are under: **http://localhost:8080/api**

#### 3. Frontend Setup (Angular)

```bash
# Navigate to frontend directory
cd angular-frontend

# Install dependencies
npm install

# Start development server
ng serve

# Or use npm script
npm start
```

Frontend will start at: **http://localhost:4200**

### Option 2: Docker Deployment

```bash
# Build and start all services
docker-compose -f docker-compose-new.yml up -d

# View logs
docker-compose -f docker-compose-new.yml logs -f

# Stop all services
docker-compose -f docker-compose-new.yml down
```

Services will be available at:
- **Frontend**: http://localhost:4200
- **Backend API**: http://localhost:8080/api
- **MongoDB**: localhost:27017

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user (protected)

### Majors
- `GET /api/majors` - Get all majors
- `GET /api/majors/{major}/stats` - Get major statistics
- `GET /api/majors/{major}/classes` - Get class rankings

### Submissions
- `POST /api/submissions/difficulty` - Submit class difficulty (protected)
- `POST /api/submissions/professor` - Submit professor rating (protected)

### Professors
- `GET /api/professors/{professor}/ratings` - Get professor ratings

### Health
- `GET /api/` - API info
- `GET /api/health` - Health check

## Development

### Backend Development

#### Running Tests
```bash
cd spring-backend
./mvnw test
```

#### Building for Production
```bash
./mvnw clean package -DskipTests
```

#### Hot Reload
Spring Boot DevTools is included for automatic restart during development.

### Frontend Development

#### Running Tests
```bash
cd angular-frontend
ng test
```

#### Building for Production
```bash
ng build --configuration production
```

#### Linting
```bash
ng lint
```

## Environment Variables

### Backend (.env)
```
MONGODB_URI=mongodb://localhost:27017/studysync
MONGODB_DATABASE=studysync
JWT_SECRET_KEY=your-secret-key-min-256-bits
PORT=8080
CORS_ORIGINS=http://localhost:4200
ENVIRONMENT=development
```

### Frontend (environment.ts)
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8080/api'
};
```

## Key Differences from React/FastAPI Version

### Backend
- **FastAPI (Python)** → **Spring Boot (Java)**
- **Pydantic models** → **Java DTOs with Bean Validation**
- **Python decorators** → **Spring annotations**
- **Motor/PyMongo** → **Spring Data MongoDB**
- **Python type hints** → **Java generics & types**

### Frontend
- **React** → **Angular**
- **JSX** → **Angular Templates**
- **useState/useEffect** → **RxJS Observables**
- **Props** → **Input/Output decorators**
- **React Context** → **Angular Services**
- **fetch API** → **HttpClient**

## Converting Remaining Components

The Login component has been converted as an example. To convert other components:

### MajorSelection Component
1. Create `angular-frontend/src/app/components/major-selection/`
2. Convert React JSX → Angular template
3. Convert state management → RxJS observables
4. Use RatingService to fetch majors

### MajorPage Component
1. Create `angular-frontend/src/app/components/major-page/`
2. Convert component logic
3. Use route parameters: `ActivatedRoute`
4. Implement rating submission forms

## Deployment

### Backend Deployment
- Package as JAR: `./mvnw clean package`
- Run: `java -jar target/studysync-backend-2.0.0.jar`
- Or use Docker image
- Environment variables via `.env` or system env

### Frontend Deployment
- Build: `ng build --configuration production`
- Output: `dist/studysync-frontend/`
- Serve with Nginx or any static host
- Or use Docker with nginx

### Cloud Deployment
See original `CLOUD_DEPLOYMENT.md` for platform-specific instructions, adapted for:
- Spring Boot on Railway/Render/AWS
- Angular on Vercel/Netlify/Cloudflare Pages

## Troubleshooting

### Port Already in Use
```bash
# Backend (8080)
lsof -ti:8080 | xargs kill

# Frontend (4200)
lsof -ti:4200 | xargs kill
```

### MongoDB Connection Issues
- Ensure MongoDB is running
- Check connection string in application.yml
- Verify network connectivity

### CORS Errors
- Check `CORS_ORIGINS` in application.yml
- Ensure frontend URL is whitelisted
- Verify Spring Security CORS configuration

## Contributing

1. Create feature branch
2. Make changes
3. Test thoroughly
4. Create pull request

## License

Educational use for UNC students.

## Migration Guide

### Converting from React to Angular

**State Management:**
```typescript
// React
const [data, setData] = useState([]);

// Angular
data$ = new BehaviorSubject<any[]>([]);
// Or use signals in Angular 16+
```

**API Calls:**
```typescript
// React
const response = await fetch(url);
const data = await response.json();

// Angular
this.http.get(url).subscribe(data => { });
```

**Routing:**
```typescript
// React Router
<Route path="/login" element={<Login />} />

// Angular Router
{ path: 'login', component: LoginComponent }
```

---

For the original Python/React version, see the `backend/` and `frontend/` directories.
