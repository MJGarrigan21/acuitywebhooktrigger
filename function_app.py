import azure.functions as func
import logging
import urllib.parse
import requests
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

ACUITY_USER_ID = "15883126"
ACUITY_API_KEY = "194f225856e29307e6da7bbe45133217"

@app.route(route="func_acuity_webhook")
def acuitywebhooktrigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Received a webhook from Acuity.')

    # Log the raw request body
    raw_body = req.get_body().decode('utf-8')  # Decoding bytes to string for better readability
    logging.info(f"Raw request body: {raw_body}")

    # Parse the URL-encoded data
    parsed_data = urllib.parse.parse_qs(raw_body)

    # Converting the parsed data to a more readable format (dictionary)
    parsed_dict = {k: v[0] for k, v in parsed_data.items()}

    # Log the parsed dictionary
    logging.info(f"Parsed request data: {parsed_dict}")

    # Store the id and calendarID values in variables
    appointment_id = parsed_dict.get('id')
    calendar_id = parsed_dict.get('calendarID')

    # Log the stored variables
    logging.info(f"Appointment ID: {appointment_id}")
    logging.info(f"Calendar ID: {calendar_id}")

    # Fetch appointment details from Acuity API
    acuity_url = f"https://acuityscheduling.com/api/v1/appointments/{appointment_id}"

    # HTTP Basic Authentication
    auth = (ACUITY_USER_ID, ACUITY_API_KEY)

    # Make the API request
    response = requests.get(acuity_url, auth=auth)

    # Check if the request was successful
    if response.status_code == 200:
        appointment_details = response.json()
        logging.info(f"Appointment details: {appointment_details}")
        
        # Parse necessary fields into variables
        appointment_id = appointment_details.get('id')
        first_name = appointment_details.get('firstName')
        last_name = appointment_details.get('lastName')
        phone = appointment_details.get('phone')
        email = appointment_details.get('email')
        date = appointment_details.get('date')
        time = appointment_details.get('time')
        end_time = appointment_details.get('endTime')
        datetime_created = appointment_details.get('datetimeCreated')
        datetime_appointment = appointment_details.get('datetime')
        appointment_type = appointment_details.get('type')
        calendar_name = appointment_details.get('calendar')
        location = appointment_details.get('location')
        price = appointment_details.get('price')
        paid = appointment_details.get('paid')
        notes = appointment_details.get('notes')
        outbound_rep = None
        
        # Parsing form values for additional information
        forms = appointment_details.get('forms', [])
        if forms:
            form_values = forms[0].get('values', [])
            for form_value in form_values:
                field_name = form_value.get('name')
                if field_name == 'Notes:':
                    notes = form_value.get('value')
                elif field_name == 'Outbound Rep':
                    outbound_rep = form_value.get('value')

        # Log the parsed variables
        logging.info(f"First Name: {first_name}")
        logging.info(f"Last Name: {last_name}")
        logging.info(f"Phone: {phone}")
        logging.info(f"Email: {email}")
        logging.info(f"Date: {date}")
        logging.info(f"Time: {time}")
        logging.info(f"End Time: {end_time}")
        logging.info(f"Datetime Created: {datetime_created}")
        logging.info(f"Datetime Appointment: {datetime_appointment}")
        logging.info(f"Appointment Type: {appointment_type}")
        logging.info(f"Calendar Name: {calendar_name}")
        logging.info(f"Location: {location}")
        logging.info(f"Price: {price}")
        logging.info(f"Paid: {paid}")
        logging.info(f"Notes: {notes}")
        logging.info(f"Outbound Rep: {outbound_rep}")

    else:
        logging.error(f"Failed to fetch appointment details. Status code: {response.status_code}")

    # Respond back with the full body content
    return func.HttpResponse(
        raw_body,
        status_code=200,
        mimetype="application/x-www-form-urlencoded"
    )
