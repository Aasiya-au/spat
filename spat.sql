-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 14, 2025 at 10:22 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `spat`
--

-- --------------------------------------------------------

--
-- Table structure for table `achievements`
--

CREATE TABLE `achievements` (
  `id` int(10) UNSIGNED NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `condition_type` enum('points','tasks','topics','leaderboard') NOT NULL,
  `condition_value` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `achievements`
--

INSERT INTO `achievements` (`id`, `name`, `description`, `condition_type`, `condition_value`) VALUES
(1, 'Quick Learner', 'Earned 50 XP', 'points', 50),
(2, 'Study Warrior', 'Earned 100 XP', 'points', 100),
(3, 'Mastermind', 'Earned 200 XP', 'points', 200),
(4, 'Task Rookie', 'Completed 10 tasks', 'tasks', 10),
(5, 'Task Champ', 'Completed 50 tasks', 'tasks', 50),
(6, 'Task Prodigy', 'Completed 100 tasks', 'tasks', 100),
(7, 'Curious Mind', 'Completed 5 topics', 'topics', 5),
(8, 'Explorer', 'Completed 10 topics', 'topics', 10),
(9, 'Scholar', 'Completed 20 topics', 'topics', 20),
(10, 'Winner', 'Finished #1 on leaderboard', 'leaderboard', 1),
(11, 'Champion', 'Finished #1 on leaderboard three times in a row', 'leaderboard', 1);

-- --------------------------------------------------------

--
-- Table structure for table `actions`
--

CREATE TABLE `actions` (
  `id` int(11) NOT NULL,
  `action_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `actions`
--

INSERT INTO `actions` (`id`, `action_name`) VALUES
(1, 'add'),
(2, 'delete'),
(3, 'update');

-- --------------------------------------------------------

--
-- Table structure for table `action_logs`
--

CREATE TABLE `action_logs` (
  `id` int(11) NOT NULL,
  `user_id` int(10) UNSIGNED NOT NULL,
  `action_id` int(11) NOT NULL,
  `target_entity_id` int(11) NOT NULL,
  `target_id` int(11) NOT NULL,
  `timestamp` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Stand-in structure for view `action_log_view`
-- (See below for the actual view)
--
CREATE TABLE `action_log_view` (
`timestamp` timestamp
,`user_id` int(10) unsigned
,`username` varchar(255)
,`action_name` varchar(50)
,`entity_name` varchar(50)
,`target_id` int(11)
);

-- --------------------------------------------------------

--
-- Table structure for table `api_logs`
--

CREATE TABLE `api_logs` (
  `id` int(11) NOT NULL,
  `timestamp` datetime DEFAULT current_timestamp(),
  `api_endpoint` varchar(255) DEFAULT NULL,
  `request_data` text DEFAULT NULL,
  `response_status` varchar(50) DEFAULT NULL,
  `response_time` int(11) DEFAULT NULL,
  `error_message` text DEFAULT NULL,
  `user_id` int(11) UNSIGNED DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `apps`
--

CREATE TABLE `apps` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `created_at` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `apps`
--

INSERT INTO `apps` (`id`, `name`, `description`, `created_at`) VALUES
(1, 'Study Planner And Tracker', 'This app is a minimalistic and efficient tool designed to help you stay organized and focused on your learning. It features a clean, easy-to-navigate interface with multiple panels, including Notes, Subjects & Tasks, a Calendar for reminders, and a Timer to log your study sessions. The app allows you to set study preferences, track progress, and stay on top of deadlines and goals, making it an ideal companion for productive study sessions.', '2025-01-01');

-- --------------------------------------------------------

--
-- Table structure for table `app_panels`
--

CREATE TABLE `app_panels` (
  `id` int(11) NOT NULL,
  `app_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `app_panels`
--

INSERT INTO `app_panels` (`id`, `app_id`, `name`, `description`) VALUES
(1, 1, 'Home', 'The home page, providing easy navigation and a summary of app features and user activity.'),
(2, 1, 'Leaderboard', 'Tracks and displays user rankings based on performance, points, or achievements.'),
(3, 1, 'Profile', 'Shows user profiles, including personal details, preferences, and study history.'),
(4, 1, 'Notes', 'Stores and organizes notes for quick reference and efficient study.'),
(5, 1, 'Study Session', 'Facilitates structured study sessions with time management and productivity tools.'),
(6, 1, 'To-Do List', 'A task manager that helps users track assignments, deadlines, and study goals.'),
(7, 1, 'Achievements', 'Displays accomplishments, milestones, and progress made by the user.'),
(8, 1, 'Appearance', 'Provides customization options, allowing users to personalize the appearance of the app.'),
(9, 1, 'Flashcards', 'A tool for creating and reviewing flashcards to aid memorization and active recall.'),
(10, 1, 'About', 'Information about the application, including usage instructions, credits, and version details.');

-- --------------------------------------------------------

--
-- Table structure for table `app_resources`
--

CREATE TABLE `app_resources` (
  `id` int(11) NOT NULL,
  `app_id` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `app_resources`
--

INSERT INTO `app_resources` (`id`, `app_id`, `name`, `description`) VALUES
(1, 1, 'Python', 'Programming Language'),
(2, 1, 'MySQL', 'Database Management System'),
(3, 1, 'PyQT', 'UI library'),
(4, 1, 'mysql-connector', 'Database library'),
(5, 1, 'VS Code', 'Code editor');

-- --------------------------------------------------------

--
-- Table structure for table `challenges`
--

CREATE TABLE `challenges` (
  `challenge_id` int(10) NOT NULL,
  `name` varchar(100) NOT NULL,
  `difficulty` enum('easy','medium','hard') NOT NULL,
  `points` int(20) NOT NULL,
  `description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `challenges`
--

INSERT INTO `challenges` (`challenge_id`, `name`, `difficulty`, `points`, `description`) VALUES
(1, 'Study for 1 Hour', 'easy', 5, 'Spend 1 hour studying any subject of your choice.'),
(2, 'Check Off 1 To-Do Item', 'easy', 5, 'Complete 1 task from your to-do list.'),
(3, 'Write a Short Note', 'easy', 5, 'Write a brief note on any topic you studied today.'),
(4, 'Review 5 Flashcards', 'easy', 5, 'Review 5 flashcards to reinforce your learning.'),
(5, 'Plan Your Study Schedule', 'easy', 5, 'Create a study schedule for the day.'),
(6, 'Study for 2 Hours', 'medium', 15, 'Dedicate 2 hours to studying without distractions.'),
(7, 'Complete 3 To-Do Items', 'medium', 15, 'Check off 3 tasks from your to-do list.'),
(8, 'Finish 1 Topic', 'medium', 15, 'Complete 1 topic in any subject.'),
(9, 'Create 10 Flashcards', 'medium', 15, 'Make 10 new flashcards for a subject.'),
(10, 'Attend a Study Event', 'medium', 15, 'Join a study session or event to collaborate with others.'),
(11, 'Study for 4 Hours', 'hard', 30, 'Spend 4 hours studying with focus and determination.'),
(12, 'Check Off 5 To-Do Items', 'hard', 30, 'Complete 5 tasks from your to-do list.'),
(13, 'Complete 2 Topics', 'hard', 30, 'Finish 2 topics in any subject.'),
(14, 'Review 20 Flashcards and Create 5', 'hard', 30, 'Review 20 flashcards and create 5 new ones.'),
(15, 'Finish a Subject', 'hard', 30, 'Complete all topics in a single subject.');

-- --------------------------------------------------------

--
-- Table structure for table `characters`
--

CREATE TABLE `characters` (
  `id` int(10) UNSIGNED NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `characters`
--

INSERT INTO `characters` (`id`, `name`) VALUES
(1, 'bunny'),
(2, 'penguin'),
(3, 'cat'),
(4, 'chick');

-- --------------------------------------------------------

--
-- Table structure for table `chat_history`
--

CREATE TABLE `chat_history` (
  `id` int(11) NOT NULL,
  `timestamp` varchar(20) NOT NULL,
  `user_query` text NOT NULL,
  `ai_response` text NOT NULL,
  `user_id` int(10) UNSIGNED DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `daily_challenge_selection`
--

CREATE TABLE `daily_challenge_selection` (
  `id` int(11) NOT NULL,
  `selection_date` date NOT NULL,
  `challenge_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `daily_challenge_selection`
--

INSERT INTO `daily_challenge_selection` (`id`, `selection_date`, `challenge_id`) VALUES
(1, '2025-04-28', 8),
(2, '2025-04-30', 5),
(3, '2025-05-02', 9),
(4, '2025-05-03', 4),
(5, '2025-05-05', 9),
(6, '2025-05-07', 15),
(7, '2025-05-08', 9),
(8, '2025-05-10', 9),
(9, '2025-05-12', 8),
(10, '2025-05-13', 1);

-- --------------------------------------------------------

--
-- Table structure for table `daily_quotes`
--

CREATE TABLE `daily_quotes` (
  `id` int(11) NOT NULL,
  `date` date NOT NULL,
  `quote` text NOT NULL,
  `author` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `developers`
--

CREATE TABLE `developers` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `role_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `developers`
--

INSERT INTO `developers` (`id`, `name`, `email`, `role_id`) VALUES
(1, 'Aasiya Asadullah', 'aasiaasadullah@gmail.com', 1),
(2, 'Mashal Zehra', 'zehramashal10@gmail.com', 2),
(3, 'Rafia Gull', 'rafiagul08@gmail.com', 4),
(4, 'Zarina Iqbal Buriro', 'zarinaiqbal04@gmail.com', 3);

-- --------------------------------------------------------

--
-- Stand-in structure for view `developer_info_view`
-- (See below for the actual view)
--
CREATE TABLE `developer_info_view` (
`id` int(11)
,`name` varchar(255)
,`email` varchar(255)
,`role_name` varchar(100)
,`description` text
);

-- --------------------------------------------------------

--
-- Table structure for table `developer_roles`
--

CREATE TABLE `developer_roles` (
  `id` int(11) NOT NULL,
  `role_name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `developer_roles`
--

INSERT INTO `developer_roles` (`id`, `role_name`, `description`) VALUES
(1, 'Project Compiler', 'Responsible for compiling, integrating, and ensuring the proper execution of project components. Focuses on code optimization and functionality.'),
(2, 'Docs Maintainer', 'Manages documentation, ensuring all project details, guidelines, and technical specifications are well-recorded and easily accessible.'),
(3, 'UI Expert', 'Specializes in user interface design, making sure the project has an intuitive, aesthetically pleasing, and accessible interface.'),
(4, 'Testing Master', 'Leads testing efforts by identifying bugs, conducting various test scenarios, and ensuring product reliability before deployment.');

-- --------------------------------------------------------

--
-- Table structure for table `error_logs`
--

CREATE TABLE `error_logs` (
  `id` int(11) NOT NULL,
  `timestamp` datetime DEFAULT current_timestamp(),
  `location` varchar(255) DEFAULT NULL,
  `message` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `error_logs`
--

INSERT INTO `error_logs` (`id`, `timestamp`, `location`, `message`) VALUES
(1, '2025-05-10 13:49:49', 'db2.py:login:84', '1146 (42S02): Table \'spat.userss\' doesn\'t exist'),
(2, '2025-05-10 13:57:28', 'db2.py:set_user_theme:745', '1452 (23000): Cannot add or update a child row: a foreign key constraint fails (`spat`.`user_theme`, CONSTRAINT `user_theme_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`))'),
(3, '2025-05-10 14:21:39', 'db2.py:add_user_achievement:556', '1062 (23000): Duplicate entry \'3-1\' for key \'PRIMARY\''),
(4, '2025-05-11 23:54:13', 'db2.py:add_task:467', 'list indices must be integers or slices, not str'),
(5, '2025-05-12 00:10:42', 'db2.py:complete_subject:272', '1054 (42S22): Unknown column \'completed\' in \'field list\''),
(6, '2025-05-12 00:18:35', 'db2.py:add_subject:235', 'list indices must be integers or slices, not str'),
(7, '2025-05-12 00:22:15', 'db2.py:add_subject:235', '\'NoneType\' object has no attribute \'get\''),
(8, '2025-05-12 01:07:19', 'db2.py:end_study_session:1129', '\'AttributeError\' object is not subscriptable'),
(9, '2025-05-12 19:51:29', 'db2.py:add_flashcard:902', '\'NoneType\' object has no attribute \'get\''),
(10, '2025-05-12 20:03:03', 'db2.py:complete_topic:407', '1054 (42S22): Unknown column \'user_id\' in \'where clause\''),
(11, '2025-05-12 21:41:12', 'db2.py:start_study_session:1113', '\'NoneType\' object has no attribute \'get\''),
(12, '2025-05-12 21:44:59', 'db2.py:start_study_session:1113', 'list indices must be integers or slices, not str'),
(13, '2025-05-12 21:45:06', 'db2.py:end_study_session:1135', '\'TypeError\' object is not subscriptable'),
(14, '2025-05-14 00:19:44', 'db3.py:get_developer:1101', 'Python type dict cannot be converted'),
(15, '2025-05-14 10:26:29', 'db2.py:start_study_session:1113', '\'NoneType\' object has no attribute \'get\''),
(16, '2025-05-14 10:26:35', 'db2.py:end_study_session:1137', '\'AttributeError\' object is not subscriptable');

-- --------------------------------------------------------

--
-- Table structure for table `flashcards`
--

CREATE TABLE `flashcards` (
  `id` int(11) NOT NULL,
  `user_id` int(10) UNSIGNED NOT NULL,
  `question` text NOT NULL,
  `answer` text NOT NULL,
  `subject_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `logins`
--

CREATE TABLE `logins` (
  `id` int(11) NOT NULL,
  `user_id` int(10) UNSIGNED NOT NULL,
  `login_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `logins`
--

INSERT INTO `logins` (`id`, `user_id`, `login_date`) VALUES
(1, 3, '2025-05-12'),
(2, 5, '2025-05-12'),
(3, 5, '2025-05-13'),
(4, 7, '2025-05-12'),
(5, 11, '2025-05-13'),
(6, 12, '2025-05-13'),
(7, 13, '2025-05-13'),
(8, 14, '2025-05-13'),
(9, 15, '2025-05-13');

-- --------------------------------------------------------

--
-- Stand-in structure for view `logins_view`
-- (See below for the actual view)
--
CREATE TABLE `logins_view` (
`user_id` int(10) unsigned
,`login_date` date
,`username` varchar(255)
);

-- --------------------------------------------------------

--
-- Table structure for table `notes`
--

CREATE TABLE `notes` (
  `id` int(11) NOT NULL,
  `user_id` int(10) UNSIGNED DEFAULT NULL,
  `title` varchar(255) NOT NULL,
  `content` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `study_sessions`
--

CREATE TABLE `study_sessions` (
  `id` int(10) UNSIGNED NOT NULL,
  `user_id` int(10) UNSIGNED NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time DEFAULT NULL,
  `duration` time DEFAULT NULL,
  `duration_in_min` int(10) UNSIGNED DEFAULT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `study_sessions`
--

INSERT INTO `study_sessions` (`id`, `user_id`, `start_time`, `end_time`, `duration`, `duration_in_min`, `date`) VALUES
(1, 3, '09:16:20', '09:16:26', '00:00:06', 0, '2025-05-12');

-- --------------------------------------------------------

--
-- Table structure for table `subjects`
--

CREATE TABLE `subjects` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `status` enum('Pending','Completed') NOT NULL DEFAULT 'Pending',
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `target_entities`
--

CREATE TABLE `target_entities` (
  `id` int(11) NOT NULL,
  `entity_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `target_entities`
--

INSERT INTO `target_entities` (`id`, `entity_name`) VALUES
(1, 'flashcards'),
(2, 'notes'),
(3, 'subjects'),
(4, 'tasks'),
(5, 'topics');

-- --------------------------------------------------------

--
-- Table structure for table `tasks`
--

CREATE TABLE `tasks` (
  `id` int(10) UNSIGNED NOT NULL,
  `title` varchar(255) NOT NULL,
  `due_date` date DEFAULT NULL,
  `status` enum('Pending','Completed') NOT NULL DEFAULT 'Pending',
  `user_id` int(10) UNSIGNED NOT NULL,
  `subject_id` int(11) NOT NULL,
  `topic_id` int(10) UNSIGNED DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `themes`
--

CREATE TABLE `themes` (
  `id` int(10) UNSIGNED NOT NULL,
  `color_1` varchar(255) NOT NULL,
  `color_2` varchar(255) NOT NULL,
  `color_3` varchar(255) NOT NULL,
  `color_4` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `themes`
--

INSERT INTO `themes` (`id`, `color_1`, `color_2`, `color_3`, `color_4`) VALUES
(1, '#F38C79', '#034C53', '#FFC1B4', '#007074'),
(2, '#89B9AD', '#FFC5C5', '#FFEBD8', '#C7DCA7'),
(3, '#FBDB93', '#BE5B50', '#8A2D3B', '#641B2E'),
(4, '#03A791', '#E9F5BE', '#81E7AF', '#F1BA88'),
(5, '#FF90BB', '#F8F8E1', '#FFC1DA', '#8ACCD5'),
(6, '#FFF0BD', '#E50046', '#FDAB9E', '#C7DB9C'),
(7, '#D76C82', '#3D0301', '#EBE8DB', '#B03052'),
(8, '#FF6363', '#BEE4D0', '#DBFFCB', '#FF8282');

-- --------------------------------------------------------

--
-- Table structure for table `topics`
--

CREATE TABLE `topics` (
  `id` int(10) UNSIGNED NOT NULL,
  `name` varchar(255) NOT NULL,
  `user_id` int(10) UNSIGNED NOT NULL,
  `subject_id` int(11) NOT NULL,
  `status` enum('Pending','Completed') NOT NULL DEFAULT 'Pending',
  `due_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(10) UNSIGNED NOT NULL,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `total_study_points` int(11) UNSIGNED NOT NULL DEFAULT 0,
  `total_tasks_completed` int(11) UNSIGNED NOT NULL DEFAULT 0,
  `total_topics_completed` int(10) UNSIGNED NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `total_study_points`, `total_tasks_completed`, `total_topics_completed`) VALUES
(1, 'Mashal', 'mashal@gmail.com', '49345334b95b286f6b287844e3d5f2c2131737b2115940a9707e940a45692639', 0, 0, 0),
(2, 'Rafia', 'rafia@gmail.com', 'b2a95962b835f71a98925b4124498c1b4b6bfaeedb972237ebb6a176fa5a6940', 0, 0, 0),
(3, 'Aasiya', 'aau@gmail.com', 'e203cdb40916311f989fc3aa5a493bb74e61062881003ae96ac865c7b4755a00', 130, 11, 7),
(4, 'Zarina', 'zarina@gmail.com', '4f54f8ca9a2480dbed7cf43e82a2da2d065a18eeae7a2725ecba4e968064dd9f', 0, 0, 0),
(5, 'aasia', 'aasia@gmail.com', 'e203cdb40916311f989fc3aa5a493bb74e61062881003ae96ac865c7b4755a00', 85, 3, 2),
(6, 'bushra', 'bbb@gmail.com', '300f329ba5580b8d19e48e76bdc31c0087d6e578725eb6ecec078e2fb6bcb261', 0, 0, 0),
(7, 'ayesha ', 'ayesha', 'bf642a5d15563defc0ec1359072978a02472f0689087d99fa951dea167825a6d', 0, 0, 0),
(8, 'abdullah ', 'abdullah@gmail.com ', '0041dec874132e09e723b1b96f44c72e507c2f5f082bbacf3cd70f1208650e12', 0, 0, 0),
(9, 'rabia', 'rabiaasadullah@gmail.com', '5ad5b26ca549464477695a6037b1bbd4056741d09de1b9dff429ca62bc48ead0', 0, 0, 0),
(10, 'ifrawrpookie', 'nifrah590@gmail.com', 'f10d4c3e75419087b54f5432a40a6c84dcd7e4c9676edf7bae9da996252da646', 15, 0, 0),
(11, 'MARYAM ', 'maryam2012@gmail.com', '67cb68c4e090ae4cd37cefb124de93b0a236542b13d113df5ed9cd7e9cb18bd7', 0, 0, 0),
(12, 'Anabia ', 'anabia@gmail.com', 'ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f', 0, 0, 0),
(13, 'waleeja', 'waleeja@gmail.com ', 'ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f', 0, 0, 0),
(14, 'Anum', 'anum@gmail.com', '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225', 0, 0, 0),
(15, 'Sara', 'sara@gmail.com', '33a7d3da476a32ac237b3f603a1be62fad00299e0d4b5a8db8d913104edec629', 0, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `user_achievements`
--

CREATE TABLE `user_achievements` (
  `user_id` int(10) UNSIGNED NOT NULL,
  `achievement_id` int(10) UNSIGNED NOT NULL,
  `achieved_at` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_achievements`
--

INSERT INTO `user_achievements` (`user_id`, `achievement_id`, `achieved_at`) VALUES
(3, 1, '2025-03-14'),
(3, 2, '2025-05-10'),
(3, 4, '2025-03-14'),
(3, 7, '2025-03-14'),
(5, 1, '2025-05-08'),
(13, 1, '2025-03-14');

-- --------------------------------------------------------

--
-- Table structure for table `user_challenges`
--

CREATE TABLE `user_challenges` (
  `id` int(11) NOT NULL,
  `user_id` int(10) UNSIGNED DEFAULT NULL,
  `challenge_id` int(11) NOT NULL,
  `completed_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_challenges`
--

INSERT INTO `user_challenges` (`id`, `user_id`, `challenge_id`, `completed_date`) VALUES
(1, 3, 5, '2025-04-30'),
(2, 3, 8, '2025-04-28'),
(3, 3, 8, '2025-05-12'),
(4, 3, 9, '2025-05-02'),
(5, 3, 9, '2025-05-08'),
(6, 3, 9, '2025-05-10'),
(7, 4, 5, '2025-04-30'),
(8, 5, 1, '2025-05-13'),
(9, 5, 4, '2025-05-03'),
(10, 5, 5, '2025-04-30'),
(11, 5, 8, '2025-05-12'),
(12, 5, 9, '2025-05-05'),
(13, 5, 9, '2025-05-08'),
(14, 5, 9, '2025-05-10'),
(15, 7, 5, '2025-04-30'),
(16, 12, 5, '2025-04-30'),
(17, 15, 5, '2025-04-30'),
(18, 15, 9, '2025-05-10'),
(19, 2, 9, '2025-05-05');

-- --------------------------------------------------------

--
-- Table structure for table `user_character`
--

CREATE TABLE `user_character` (
  `user_id` int(10) UNSIGNED NOT NULL,
  `character_id` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_character`
--

INSERT INTO `user_character` (`user_id`, `character_id`) VALUES
(3, 1),
(7, 1),
(5, 2),
(9, 3),
(10, 4);

-- --------------------------------------------------------

--
-- Stand-in structure for view `user_subject_overview`
-- (See below for the actual view)
--
CREATE TABLE `user_subject_overview` (
`user_id` int(10) unsigned
,`username` varchar(255)
,`user_email` varchar(255)
,`subject_id` int(11)
,`subject_name` varchar(255)
,`topic_id` int(10) unsigned
,`topic_name` varchar(255)
,`task_id` int(10) unsigned
,`task_title` varchar(255)
,`status` enum('Pending','Completed')
);

-- --------------------------------------------------------

--
-- Table structure for table `user_theme`
--

CREATE TABLE `user_theme` (
  `user_id` int(10) UNSIGNED NOT NULL,
  `theme_id` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_theme`
--

INSERT INTO `user_theme` (`user_id`, `theme_id`) VALUES
(10, 1),
(7, 2),
(9, 3),
(3, 4),
(5, 7);

-- --------------------------------------------------------

--
-- Structure for view `action_log_view`
--
DROP TABLE IF EXISTS `action_log_view`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `action_log_view`  AS SELECT `al`.`timestamp` AS `timestamp`, `u`.`id` AS `user_id`, `u`.`username` AS `username`, `a`.`action_name` AS `action_name`, `te`.`entity_name` AS `entity_name`, `al`.`target_id` AS `target_id` FROM (((`action_logs` `al` join `users` `u` on(`al`.`user_id` = `u`.`id`)) join `actions` `a` on(`al`.`action_id` = `a`.`id`)) join `target_entities` `te` on(`al`.`target_entity_id` = `te`.`id`)) ORDER BY `al`.`timestamp` DESC ;

-- --------------------------------------------------------

--
-- Structure for view `developer_info_view`
--
DROP TABLE IF EXISTS `developer_info_view`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `developer_info_view`  AS SELECT `developers`.`id` AS `id`, `developers`.`name` AS `name`, `developers`.`email` AS `email`, `developer_roles`.`role_name` AS `role_name`, `developer_roles`.`description` AS `description` FROM (`developers` join `developer_roles` on(`developers`.`role_id` = `developer_roles`.`id`)) ;

-- --------------------------------------------------------

--
-- Structure for view `logins_view`
--
DROP TABLE IF EXISTS `logins_view`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `logins_view`  AS SELECT `l`.`user_id` AS `user_id`, `l`.`login_date` AS `login_date`, `u`.`username` AS `username` FROM (`logins` `l` join `users` `u` on(`l`.`user_id` = `u`.`id`)) ;

-- --------------------------------------------------------

--
-- Structure for view `user_subject_overview`
--
DROP TABLE IF EXISTS `user_subject_overview`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `user_subject_overview`  AS SELECT `users`.`id` AS `user_id`, `users`.`username` AS `username`, `users`.`email` AS `user_email`, `subjects`.`id` AS `subject_id`, `subjects`.`name` AS `subject_name`, `topics`.`id` AS `topic_id`, `topics`.`name` AS `topic_name`, `tasks`.`id` AS `task_id`, `tasks`.`title` AS `task_title`, `tasks`.`status` AS `status` FROM (((`users` left join `subjects` on(`subjects`.`user_id` = `users`.`id`)) left join `topics` on(`topics`.`subject_id` = `subjects`.`id`)) left join `tasks` on(`tasks`.`subject_id` = `subjects`.`id`)) ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `achievements`
--
ALTER TABLE `achievements`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `actions`
--
ALTER TABLE `actions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `action_name` (`action_name`);

--
-- Indexes for table `action_logs`
--
ALTER TABLE `action_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `action_id` (`action_id`),
  ADD KEY `target_entity_id` (`target_entity_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `api_logs`
--
ALTER TABLE `api_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `api_fk1` (`user_id`);

--
-- Indexes for table `apps`
--
ALTER TABLE `apps`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `app_panels`
--
ALTER TABLE `app_panels`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_id` (`app_id`);

--
-- Indexes for table `app_resources`
--
ALTER TABLE `app_resources`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_res_fk1` (`app_id`);

--
-- Indexes for table `challenges`
--
ALTER TABLE `challenges`
  ADD PRIMARY KEY (`challenge_id`);

--
-- Indexes for table `characters`
--
ALTER TABLE `characters`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `chat_history`
--
ALTER TABLE `chat_history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `chat_fk1` (`user_id`);

--
-- Indexes for table `daily_challenge_selection`
--
ALTER TABLE `daily_challenge_selection`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_selection_date` (`selection_date`),
  ADD KEY `daily_fk1` (`challenge_id`);

--
-- Indexes for table `daily_quotes`
--
ALTER TABLE `daily_quotes`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `developers`
--
ALTER TABLE `developers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `role_id` (`role_id`);

--
-- Indexes for table `developer_roles`
--
ALTER TABLE `developer_roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `role_name` (`role_name`);

--
-- Indexes for table `error_logs`
--
ALTER TABLE `error_logs`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `flashcards`
--
ALTER TABLE `flashcards`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `flashcards_ibfk_2` (`subject_id`);

--
-- Indexes for table `logins`
--
ALTER TABLE `logins`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`,`login_date`);

--
-- Indexes for table `notes`
--
ALTER TABLE `notes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `notes_fk1` (`user_id`);

--
-- Indexes for table `study_sessions`
--
ALTER TABLE `study_sessions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `subjects`
--
ALTER TABLE `subjects`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `target_entities`
--
ALTER TABLE `target_entities`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `entity_name` (`entity_name`);

--
-- Indexes for table `tasks`
--
ALTER TABLE `tasks`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `subject_id` (`subject_id`),
  ADD KEY `fk_tasks_topic` (`topic_id`);

--
-- Indexes for table `themes`
--
ALTER TABLE `themes`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `topics`
--
ALTER TABLE `topics`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `subject_id` (`subject_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `user_achievements`
--
ALTER TABLE `user_achievements`
  ADD PRIMARY KEY (`user_id`,`achievement_id`),
  ADD KEY `achievement_id` (`achievement_id`);

--
-- Indexes for table `user_challenges`
--
ALTER TABLE `user_challenges`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_challenge_date` (`user_id`,`challenge_id`,`completed_date`);

--
-- Indexes for table `user_character`
--
ALTER TABLE `user_character`
  ADD PRIMARY KEY (`user_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `character_id` (`character_id`);

--
-- Indexes for table `user_theme`
--
ALTER TABLE `user_theme`
  ADD PRIMARY KEY (`user_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `theme_id` (`theme_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `actions`
--
ALTER TABLE `actions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `action_logs`
--
ALTER TABLE `action_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- AUTO_INCREMENT for table `api_logs`
--
ALTER TABLE `api_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- AUTO_INCREMENT for table `apps`
--
ALTER TABLE `apps`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `app_panels`
--
ALTER TABLE `app_panels`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `app_resources`
--
ALTER TABLE `app_resources`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `challenges`
--
ALTER TABLE `challenges`
  MODIFY `challenge_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `characters`
--
ALTER TABLE `characters`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `chat_history`
--
ALTER TABLE `chat_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- AUTO_INCREMENT for table `daily_challenge_selection`
--
ALTER TABLE `daily_challenge_selection`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `daily_quotes`
--
ALTER TABLE `daily_quotes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- AUTO_INCREMENT for table `developers`
--
ALTER TABLE `developers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `developer_roles`
--
ALTER TABLE `developer_roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `error_logs`
--
ALTER TABLE `error_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `flashcards`
--
ALTER TABLE `flashcards`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- AUTO_INCREMENT for table `logins`
--
ALTER TABLE `logins`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `notes`
--
ALTER TABLE `notes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- AUTO_INCREMENT for table `study_sessions`
--
ALTER TABLE `study_sessions`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `subjects`
--
ALTER TABLE `subjects`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- AUTO_INCREMENT for table `target_entities`
--
ALTER TABLE `target_entities`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `tasks`
--
ALTER TABLE `tasks`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- AUTO_INCREMENT for table `themes`
--
ALTER TABLE `themes`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `topics`
--
ALTER TABLE `topics`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `user_challenges`
--
ALTER TABLE `user_challenges`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `action_logs`
--
ALTER TABLE `action_logs`
  ADD CONSTRAINT `action_logs_ibfk_1` FOREIGN KEY (`action_id`) REFERENCES `actions` (`id`),
  ADD CONSTRAINT `action_logs_ibfk_2` FOREIGN KEY (`target_entity_id`) REFERENCES `target_entities` (`id`),
  ADD CONSTRAINT `action_logs_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `api_logs`
--
ALTER TABLE `api_logs`
  ADD CONSTRAINT `api_fk1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `app_panels`
--
ALTER TABLE `app_panels`
  ADD CONSTRAINT `app_panels_ibfk_1` FOREIGN KEY (`app_id`) REFERENCES `apps` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `app_resources`
--
ALTER TABLE `app_resources`
  ADD CONSTRAINT `app_res_fk1` FOREIGN KEY (`app_id`) REFERENCES `apps` (`id`);

--
-- Constraints for table `chat_history`
--
ALTER TABLE `chat_history`
  ADD CONSTRAINT `chat_fk1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `daily_challenge_selection`
--
ALTER TABLE `daily_challenge_selection`
  ADD CONSTRAINT `daily_fk1` FOREIGN KEY (`challenge_id`) REFERENCES `challenges` (`challenge_id`);

--
-- Constraints for table `developers`
--
ALTER TABLE `developers`
  ADD CONSTRAINT `developers_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `developer_roles` (`id`);

--
-- Constraints for table `flashcards`
--
ALTER TABLE `flashcards`
  ADD CONSTRAINT `flashcards_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `flashcards_ibfk_2` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `logins`
--
ALTER TABLE `logins`
  ADD CONSTRAINT `logins_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `notes`
--
ALTER TABLE `notes`
  ADD CONSTRAINT `notes_fk1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `study_sessions`
--
ALTER TABLE `study_sessions`
  ADD CONSTRAINT `study_sessions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `tasks`
--
ALTER TABLE `tasks`
  ADD CONSTRAINT `fk_tasks_topic` FOREIGN KEY (`topic_id`) REFERENCES `topics` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `subject_id` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `topics`
--
ALTER TABLE `topics`
  ADD CONSTRAINT `topics_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `topics_ibfk_2` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `user_achievements`
--
ALTER TABLE `user_achievements`
  ADD CONSTRAINT `user_achievements_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `user_achievements_ibfk_2` FOREIGN KEY (`achievement_id`) REFERENCES `achievements` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `user_challenges`
--
ALTER TABLE `user_challenges`
  ADD CONSTRAINT `fk1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `user_character`
--
ALTER TABLE `user_character`
  ADD CONSTRAINT `user_character_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `user_character_ibfk_2` FOREIGN KEY (`character_id`) REFERENCES `characters` (`id`);

--
-- Constraints for table `user_theme`
--
ALTER TABLE `user_theme`
  ADD CONSTRAINT `user_theme_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `user_theme_ibfk_2` FOREIGN KEY (`theme_id`) REFERENCES `themes` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
