from django.db import migrations


def create_present_ejeh(apps, schema_editor):
    EjehProfile = apps.get_model("palace", "EjehProfile")

    # If a present Ejeh already exists, don't create another
    if EjehProfile.objects.filter(reign_status="present", is_active=True).exists():
        return

    EjehProfile.objects.create(
        full_name="Alhaji Abubakar Sadiq Ahmed Yakubu",
        title="HRH",
        royal_title="Ejeh Ankpa IV",
        full_title_and_honours=(
            "His Royal Highness, Alhaji Abubakar Sadiq Ahmed Yakubu, "
            "The Ejeh Ankpa IV"
        ),
        reign_status="present",
        reign_start="2021-10-21",
        reign_number=4,
        birth_date="1978-04-09",
        birth_place="Kano State, North-west Nigeria",
        biography=(
            "The Ejeh Ankpa IV, His Royal Highness, Alhaji Abubakar Ahmed Yakubu "
            "was born into the family of Late Ejeh Ahmadu Yakubu on the 9th day "
            "of April, 1978 in Kano State, North-west Nigeria. Alhaji Abubakar "
            "descends from a lineage marked with combination of royal blood and "
            "humanitarian service."
        ),
        early_life=(
            "He started his early life with a Primary Education at the Magwan "
            "Special Primary School, Kano, from 1983 to 1988 and a secondary "
            "education at the prestigious Government Secondary School, Kawaji, "
            "Kano State between 1989 to 1994."
        ),
        education=(
            "B.Sc. Business Administration: Enugu State University of Science "
            "and Technology, Enugu (1999-2004); Postgraduate studies in "
            "Management Information System (MIS), Meridian College Greenwich, "
            "London (2006-2007)."
        ),
        occupation_before_throne=(
            "Business Development and project coordination roles in the energy "
            "and infrastructure sectors prior to ascending the throne."
        ),
        achievements=(
            "Recognized for contributions to economic development projects and "
            "community service across Kogi State and beyond."
        ),
        legacy=(
            "Committed to bequeathing a greater Ankpa to generations to come, "
            "with a strong focus on youth empowerment and humanitarian service."
        ),
        motto="He will bequeath a greater Ankpa to generations to come",
        hobbies="Charity works, reading and intelligent interactions",
        countries_visited=(
            "UK, Germany, Kenya, Russia, India, Qatar, USA, Saudi Arabia, "
            "Ethiopia, Australia, Spain, Turkey"
        ),
        display_order=1,
        is_active=True,
    )


def delete_present_ejeh(apps, schema_editor):
    EjehProfile = apps.get_model("palace", "EjehProfile")
    EjehProfile.objects.filter(
        full_name="Alhaji Abubakar Sadiq Ahmed Yakubu",
        royal_title="Ejeh Ankpa IV",
        reign_status="present",
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("palace", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_present_ejeh, delete_present_ejeh),
    ]


