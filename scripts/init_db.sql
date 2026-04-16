-- HireReady MySQL starter schema (Phase 1)
CREATE DATABASE IF NOT EXISTS hireready;
USE hireready;

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  roll_no VARCHAR(30) NOT NULL UNIQUE,
  email VARCHAR(120) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(20) NOT NULL DEFAULT 'student',
  cgpa DECIMAL(4,2) NULL,
  skills TEXT NULL,
  phone VARCHAR(30) NULL,
  gender VARCHAR(20) NULL,
  branch VARCHAR(120) NULL,
  current_year VARCHAR(20) NULL
);

CREATE TABLE IF NOT EXISTS questions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  company VARCHAR(120) NOT NULL,
  category VARCHAR(120) NOT NULL,
  difficulty VARCHAR(20) NOT NULL DEFAULT 'Medium',
  prompt TEXT NOT NULL,
  option_a TEXT NOT NULL,
  option_b TEXT NOT NULL,
  option_c TEXT NOT NULL,
  option_d TEXT NOT NULL,
  correct_option CHAR(1) NOT NULL,
  explanation TEXT NULL
);

CREATE TABLE IF NOT EXISTS mock_tests (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(160) NOT NULL,
  company VARCHAR(120) NOT NULL DEFAULT 'General',
  duration_minutes INT NOT NULL DEFAULT 20,
  total_questions INT NOT NULL DEFAULT 20
);

CREATE TABLE IF NOT EXISTS mock_test_questions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  mock_test_id INT NOT NULL,
  question_id INT NOT NULL,
  position INT NOT NULL,
  FOREIGN KEY (mock_test_id) REFERENCES mock_tests(id) ON DELETE CASCADE,
  FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS jobs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  company VARCHAR(120) NOT NULL,
  role VARCHAR(160) NOT NULL,
  job_type VARCHAR(40) NOT NULL DEFAULT 'Full-time',
  location VARCHAR(120) NULL,
  days_left INT NULL,
  status VARCHAR(40) NOT NULL DEFAULT 'Open'
);

CREATE TABLE IF NOT EXISTS applications (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  job_id INT NOT NULL,
  status VARCHAR(40) NOT NULL DEFAULT 'Applied',
  applied_on DATETIME NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
  UNIQUE KEY uniq_user_job (user_id, job_id)
);

CREATE TABLE IF NOT EXISTS mock_test_attempts (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  mock_test_id INT NOT NULL,
  correct_count INT NOT NULL DEFAULT 0,
  total_questions INT NOT NULL DEFAULT 0,
  score_percent DOUBLE NOT NULL DEFAULT 0,
  submitted_at DATETIME NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (mock_test_id) REFERENCES mock_tests(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS interview_schedules (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  company VARCHAR(120) NOT NULL,
  role VARCHAR(160) NOT NULL,
  interview_type VARCHAR(60) NOT NULL DEFAULT 'Technical',
  scheduled_at DATETIME NOT NULL,
  mode VARCHAR(40) NOT NULL DEFAULT 'Virtual',
  location VARCHAR(160) NULL,
  status VARCHAR(40) NOT NULL DEFAULT 'Scheduled',
  notes TEXT NULL,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
