INSERT INTO users (full_name, email, course, student_level, password_hash) VALUES
('Daniel Okafor', 'daniel.okafor@student.example.com', 'Cyber Security', '200', crypt('Study@123', gen_salt('bf'))),
('Grace Nwosu', 'grace.nwosu@student.example.com', 'Computer Science', '300', crypt('Study@123', gen_salt('bf'))),
('Michael Eze', 'michael.eze@student.example.com', 'Cyber Security', '200', crypt('Study@123', gen_salt('bf'))),
('Jessica Umeh', 'jessica.umeh@student.example.com', 'Computer Science', '300', crypt('Study@123', gen_salt('bf'))),
('Samuel Okeke', 'samuel.okeke@student.example.com', 'Cyber Security', '200', crypt('Study@123', gen_salt('bf'))),
('Amara Chukwu', 'amara.chukwu@student.example.com', 'Computer Science', '300', crypt('Study@123', gen_salt('bf'))),
('David Brown', 'david.brown@student.example.com', 'Cyber Security', '200', crypt('Study@123', gen_salt('bf'))),
('Emily Carter', 'emily.carter@student.example.com', 'Computer Science', '300', crypt('Study@123', gen_salt('bf'))),
('Chinedu Nnamani', 'chinedu.nnamani@student.example.com', 'Cyber Security', '200', crypt('Study@123', gen_salt('bf'))),
('Ngozi Ihejirika', 'ngozi.ihejirika@student.example.com', 'Computer Science', '300', crypt('Study@123', gen_salt('bf'))),
('James Wilson', 'james.wilson@student.example.com', 'Cyber Security', '200', crypt('Study@123', gen_salt('bf'))),
('Sophia Bennett', 'sophia.bennett@student.example.com', 'Computer Science', '300', crypt('Study@123', gen_salt('bf')));

INSERT INTO study_groups (course_code, group_name, created_by) VALUES
('COS 201', 'Data Structures Study Group', 1),
('CYB 201', 'Cybersecurity Fundamentals Group', 2),
('CYB 203', 'Network Security Study Group', 8),
('CYB 205', 'Digital Forensics Study Group', 10);

INSERT INTO group_members (group_id, user_id) VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
(2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7),
(3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 1),
(4, 10), (4, 11), (4, 12), (4, 1), (4, 2), (4, 3);

INSERT INTO availability (user_id, day_of_week, start_time, end_time) VALUES
(1, 1, '17:00', '18:00'), (1, 3, '14:00', '16:00'), (1, 5, '18:00', '20:00'), (1, 2, '18:00', '19:00'),
(2, 1, '17:00', '18:00'), (2, 3, '16:00', '18:00'), (2, 6, '10:00', '12:00'), (2, 2, '18:00', '19:00'),
(3, 1, '17:00', '18:00'), (3, 3, '16:00', '18:00'), (3, 5, '15:00', '17:00'), (3, 2, '18:00', '19:00'),
(4, 1, '17:00', '18:00'), (4, 3, '16:00', '18:00'), (4, 6, '10:00', '12:00'),
(5, 1, '17:00', '18:00'), (5, 3, '16:00', '18:00'), (5, 6, '10:00', '12:00'),
(6, 1, '17:00', '18:00'), (6, 3, '16:00', '18:00'), (6, 6, '10:00', '12:00'),
(7, 1, '14:00', '16:00'), (7, 3, '16:00', '18:00'), (7, 6, '10:00', '12:00'),
(8, 2, '10:00', '12:00'), (8, 4, '14:00', '16:00'), (8, 5, '13:00', '15:00'),
(9, 3, '11:00', '13:00'), (9, 4, '14:00', '16:00'), (9, 6, '09:00', '11:00'),
(10, 2, '10:00', '12:00'), (10, 5, '13:00', '15:00'), (10, 7, '09:00', '11:00'), (10, 2, '18:00', '19:00'),
(11, 3, '11:00', '13:00'), (11, 4, '15:00', '17:00'), (11, 7, '09:00', '11:00'), (11, 2, '18:00', '19:00'),
(12, 2, '10:00', '12:00'), (12, 4, '15:00', '17:00'), (12, 5, '13:00', '15:00'), (12, 2, '18:00', '19:00');

INSERT INTO study_sessions (group_id, topic, session_date, start_time, end_time, location, meeting_link, status) VALUES
(1, 'Arrays, Linked Lists and Time Complexity', '2026-09-15', '17:00', '19:00', 'Computer Lab 1', 'https://meet.example.com/cos201', 'Completed'),
(2, 'Introduction to Cybersecurity Threats', '2026-09-17', '18:00', '20:00', 'ICT Seminar Room', 'https://meet.example.com/cyb201-a', 'Completed'),
(2, 'Network Attacks and Defence', '2026-09-19', '16:00', '18:00', 'ICT Seminar Room', 'https://meet.example.com/cyb201-b', 'Completed'),
(3, 'Database Revision', '2026-09-22', '15:00', '17:00', 'Library Room 3', 'https://meet.example.com/cyb203', 'Completed'),
(4, 'Digital Evidence Collection', '2026-09-24', '18:00', '20:00', 'Forensics Lab', 'https://meet.example.com/cyb205-a', 'Completed'),
(4, 'Access Control and Authentication', '2026-09-26', '17:00', '19:00', 'Forensics Lab', 'https://meet.example.com/cyb205-b', 'Planned');

INSERT INTO attendance (session_id, user_id, attendance_status) VALUES
(1, 1, 'Present'), (1, 2, 'Present'), (1, 3, 'Late'), (1, 4, 'Present'), (1, 5, 'Present'),
(2, 2, 'Present'), (2, 3, 'Absent'), (2, 4, 'Present'), (2, 5, 'Late'), (2, 6, 'Present'),
(3, 2, 'Present'), (3, 4, 'Present'), (3, 5, 'Excused'), (3, 6, 'Present'), (3, 7, 'Absent'),
(4, 8, 'Present'), (4, 9, 'Present'), (4, 10, 'Late'), (4, 11, 'Present'), (4, 12, 'Excused'),
(5, 10, 'Present'), (5, 11, 'Present'), (5, 12, 'Late'), (5, 1, 'Present'), (5, 2, 'Absent'),
(6, 10, 'Present'), (6, 11, 'Excused'), (6, 12, 'Present'), (6, 1, 'Late'), (6, 2, 'Present');
