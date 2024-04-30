import os
import time
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import os
import json

# import self created python package
from list_of_us_universities_with_state_code.main import get_state_code_of_university

from backend import settings

# Create your views here.
# here we will write our view


def say_hello(request):
    return HttpResponse("Hello")


def csv_to_json(csv_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_path, encoding="ISO-8859-1")

    # Convert the DataFrame to JSON
    json_data = df.to_json(orient="records")

    # dump the data
    json_data = json.loads(json_data)

    # return the JSON
    return json_data


@csrf_exempt
def upload_csv(request):
    current_time = round(time.time())
    path = ""
    if request.method == "POST":
        for key, file in request.FILES.items():
            path = os.path.join(
                settings.MEDIA_ROOT, "file_" + str(current_time) + "_" + file.name
            )
            with open(path, "wb") as dest:  # Open the file in binary mode
                if file.multiple_chunks():
                    for chunk in file.chunks():
                        dest.write(chunk)
                else:
                    dest.write(file.read())

        # we are here, means we have the file saved in media folder
        # Convert CSV files to JSON
        json_data = csv_to_json(path)
        print("json_data: ", json_data)

        # final json
        final_json = []
        # now lets iterate over json data and try to map the json_data with our schema
        for row in json_data:
            # keys to manage uniquely
            # keep the keys in lowercase for mapping purpose
            key_count = {"class": [], "school": [], "state": []}
            # name must be concatinated, as the name suggests the same human entity
            full_name = []
            for key in row:
                print("key: ", key)
                # now map the keys and find repeatation in similarity
                if "class" in key.lower():
                    key_count["class"].append(row.get(key))
                if "school" in key.lower():
                    key_count["school"].append(row.get(key))
                if (
                    "state" in key.lower()
                    or "location" in key.lower()
                    or "address" in key.lower()
                ):
                    key_count["state"].append(row.get(key))
                if "name" in key.lower():
                    full_name.append(row.get(key))

            # now we have all the possible entries, now create combinations
            for c in key_count["class"]:
                print("c: ", c)
                for s in key_count["school"]:
                    print("s: ", s)
                    for st in key_count["state"]:
                        print("st: ", st)
                        new_row = {}
                        new_row["Class"] = c
                        new_row["School"] = s
                        new_row["State"] = get_state_code_of_university(s)[s]
                        new_row["Name"] = " ".join(full_name)
                        # append this to final json
                        final_json.append(new_row)

        # print the final json
        print("final_json: ", final_json)
        # Return a response object that indicates the success of the file upload.
        return JsonResponse(
            {"message": "File uploaded successfully", "json_data": final_json},
            status=200,
        )
    else:
        return JsonResponse(
            {"message": "Please upload a file via post request"}, status=400
        )
