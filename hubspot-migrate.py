import json
import csv
from datetime import datetime

def load_users_from_csv(filename):
    users = {}
    try:
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user_id = row['User ID']
                first_name = row['First Name']
                last_name = row['Last Name']
                users[user_id] = f"{first_name} {last_name}"
    except FileNotFoundError:
        print(f"User CSV file '{filename}' not found.")
    return users

def extract_email_and_note_data(json_data, users):
    data = []
    for activity in json_data:
        if 'engagement' in activity and 'metadata' in activity:
            engagement = activity['engagement']
            metadata = activity['metadata']
            
            email_activity_date = ''
            note_activity_date = ''
            email_body = ''
            note_body = ''
            email_subject = ''
            email_direction = ''
            
            timestamp = engagement.get('timestamp', '')
            
            if timestamp:
                activity_date = datetime.strptime(timestamp, '%b %d, %Y %I:%M %p %Z').strftime('%Y-%m-%d')
            
            if engagement.get('type') == 'EMAIL':
                if isinstance(metadata['from'], dict):
                    from_email = metadata['from'].get('email', '')
                else:
                    from_email = metadata['from']
                
                if not from_email:
                    continue  # Skip the activity if 'from' is empty
                
                to_emails = [to['email'] for to in metadata.get('to', [])]
                email_subject = metadata.get('subject', '')
                body = metadata.get('text', '')
                
                email_body = f"From: {from_email}\nTo: {', '.join(to_emails)}\n\n{body}"
                email_activity_date = activity_date
                email_direction = 'Outgoing' if from_email == email else 'Incoming'
            
            elif engagement.get('type') == 'NOTE':
                created_by_id = str(engagement.get('createdBy', ''))
                created_by_name = users.get(created_by_id, 'Unknown User')
                
                note_body = metadata.get('body', '')
                note_body = f"{created_by_name}: {note_body}"
                note_activity_date = activity_date
            
            else:
                continue  # Skip the activity if it's not an email or a note
            
            data.append([email_activity_date, note_activity_date, email_subject, email_body, note_body, email_direction])
    
    return data

def write_to_csv(data, email, csv_filename):
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Email', 'Email Activity Date', 'Note Activity Date', 'Email Subject', 'Email Body', 'Note Body', 'Email Direction'])
        for row in data:
            writer.writerow([email] + row)

# Get the JSON filename from the user
json_filename = input("Enter the JSON file name: ")

# Get the email address from the user
email = input("Enter the email address to prepend to each row: ")

# Get the user CSV filename from the user
user_csv_filename = input("Enter the user CSV file name: ")

try:
    # Load users from the CSV file
    users = load_users_from_csv(user_csv_filename)

    # Read the JSON data from the file
    with open(json_filename, 'r') as json_file:
        json_data = json.load(json_file)

    # Extract the email and note data
    data = extract_email_and_note_data(json_data, users)

    # Write the data to a CSV file with the email address prepended
    write_to_csv(data, email, 'data.csv')

    print("CSV file 'data.csv' created successfully.")

except FileNotFoundError:
    print(f"File '{json_filename}' not found.")

except json.JSONDecodeError:
    print(f"Invalid JSON format in file '{json_filename}'.")

except Exception as e:
    print(f"An error occurred: {str(e)}")
