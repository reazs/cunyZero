import datetime as dt


day_of_week = dt.datetime.now().weekday()
first_class_day = "Mon"
second_class_day = "Wed"


classes = [

    {
        "class_name": "CSc 33200",
        "class_id": "1fighd",
        "instructor": "staff",
        "day_of_week": f"{first_class_day} {second_class_day}",
        "time": "10:00AM-11:30AM",
        "seat": "24/32",
        "status": "open"

    },
    {
        "class_name": "CSc 22000",
        "class_id": "1ajkfhak",
        "instructor": "staff",
        "day_of_week": f"{first_class_day} {second_class_day}",
        "time": "2:00PM-3:45PM",
        "seat": "43/54",
        "status": "open"

    },
    {
        "class_name": "CSc 30400",
        "class_id": "kadfd342s",
        "instructor": "staff",
        "day_of_week": f"{first_class_day} {second_class_day}",
        "time": "10:00AM-11:30AM",
        "seat": "15/29",
        "status": "open"

    },
    {
        "class_name": "CSc 30100",
        "class_id": "19jkaf",
        "instructor": "staff",
        "day_of_week": f"Tus Thus",
        "time": "10:00AM-11:30AM",
        "seat": "18/18",
        "status": "close"

    },
    {
        "class_name": "Csc 11400",
        "class_id": "scse9034d",
        "instructor": "staff",
        "day_of_week": f"Fri",
        "time": "9:00AM-11:00Am",
        "seat": "28/35",
        "status": "open"
    }

]