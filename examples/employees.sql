-- Create the employees table
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    department TEXT NOT NULL
);

-- Insert data into the employees table
INSERT INTO employees (employee_id, first_name, last_name, email, department) VALUES
(1, 'John', 'Doe', 'john.doe@example.com', 'Sales'),
(2, 'Jane', 'Smith', 'jane.smith@example.com', 'Marketing'),
(3, 'Bob', 'Johnson', 'bob.johnson@example.com', 'Development'),
(4, 'Alice', 'Brown', 'alice.brown@example.com', 'Support');
