from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from location.models import Province, District, Municipality, Ward
from location.province_data import province_list


class Command(BaseCommand):
    help = "Load countries, provinces, districts, municipalities and VDCs"

    def handle(self, *args, **options):
        actor = get_user_model().objects.filter(is_superuser=True).first()
        for province in province_list:
            province_obj, created = Province.objects.get_or_create(
                name=province["name"] + " Pradesh",
                nepali_name=province["nepali_name"] + " प्रदेश",
                number=province["number"],
            )
            self.stdout.write(self.style.SUCCESS(
                f"Province {province_obj.name} created successfully"
            ))
            for district in province["districts"]:
                district_obj, created = District.objects.get_or_create(
                    name=district["name"],
                    nepali_name=district["nepali_name"],
                    province=province_obj,
                )
                self.stdout.write(self.style.SUCCESS(
                    f"District {district_obj.name} created successfully"
                ))
                for municipality in district["municipalities"]:
                    municipality_obj, created = Municipality.objects.get_or_create(
                        name=municipality["name"],
                        nepali_name=municipality["nepali_name"],
                        district=district_obj,
                        latitude=municipality["lat_lang"].split(",")[0],
                        longitude=municipality["lat_lang"].split(",")[1],
                        created_by=actor, updated_by=actor
                    )
                    self.stdout.write(self.style.SUCCESS(
                        f"Municipality {municipality_obj.name} created successfully"
                    ))
                    for ward in municipality["wards"]:
                        ward_obj, created = Ward.objects.get_or_create(
                            name=ward["name"],
                            nepali_name=ward["nepali_name"],
                            number=ward["number"],
                            municipality=municipality_obj,
                        )
                        self.stdout.write(self.style.SUCCESS(
                            f"Ward {ward_obj.name} created successfully"
                        ))
