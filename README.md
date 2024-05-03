# hubspot-migrate
Migrate emails and notes for a contact from one hubspot account to another.

Hubspot lets you export activities associated with a contact as a JSON, but [there seems to be no cheap and easy way to import the JSON back into Hubspot](https://community.hubspot.com/t5/CRM/Moving-data-from-one-Hubspot-account-to-another/m-p/269684). So, I had AI write me a python script.

This process assumes that you are a super admin and that you're moving activities for a given user from one Hubspot account (source account) to another Hubspot account (receiving account) where the users from the source account are not in the receiving account.

## 1. Export from Source Hubspot

1. Follow [Hubspot's instructions to **export your user data**](https://knowledge.hubspot.com/user-management/export-users). You probably want your notes to be attributed to whoever wrote the note in the source account. When you export the contact activities, the associations will use the source account's user IDs, which are numeric. So to match up the IDs to the first and last names, you need this user file. When you download it, give it a nice short name like users.csv
2. Follow [Hubspot's instructions to **export contact activities**](https://knowledge.hubspot.com/import-and-export/export-contact-data). Select "Contact Activities" in the export options.

## 2. Run the script to generate an importable CSV

The script will prompt you for the path to the **users file** and the **contact_activities.json** file, as well as the **email of the contact in the receiving database**. This email is needed to create the association to the contact.

## 3. Import into Receiving Hubspot

Follow [Hubspot's instructions for a single-file, multi-object import](https://knowledge.hubspot.com/import-and-export/import-objects).

1. How would you like to start?
    Select **Import file from computer**
1. How many files are you importing?
    Select **One File**
1. How many objects are you importing?
    Select **Multiple Objects**
1. Select the objects you'd like to import and associate
    Select **Contacts**
    Then select **Emails** and **Notes** under Activities
1. Upload your files
    For "Choose how to import Contacts" select "Update existing Contacts only"

The next screen requires you to map the csv columns. Because the csv has both note fields and email fields, the fields for each type are separate. Map them like this:

<img width="1024" alt="Screenshot 2024-05-03 at 7 22 11 PM" src="https://github.com/bomeejung/hubspot-migrate/assets/86614412/d4d1bd90-04eb-480d-858c-92047c2fe051">

There will be some warnings because the Notes entries won't have Email required fields and vice versa. You can ignore the warnings.



