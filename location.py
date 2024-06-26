from flask import request
from linebot.models import *
import os,time,googlemaps,json

class Location:
    def __init__(self):
        self.GOOGLE_MAP_API_KEY = os.getenv('GOOGLE_MAP_API_KEY')
        self.GMap = googlemaps.Client(key=self.GOOGLE_MAP_API_KEY)

    def map_location(self, event):
        body = request.get_data(as_text=True)
        json_data = json.loads(body)
        Mylocation = json_data['events'][0]['message']['address']
        print(Mylocation)
        geocode_result = self.GMap.geocode(Mylocation)
        places_result = self.GMap.places_nearby(location=geocode_result[0]['geometry']['location'] , keyword='健身', radius=500)
        print(geocode_result[0]['geometry']['location'])
        pids = []
        for place in places_result["results"]:
            pids.append([place['place_id']])
        gym_info = []
        for id in pids:
            print('loning')
            gym_info.append(self.GMap.place(place_id = id,language='zh-TW')['result'])
            time.sleep(0.3)
        return self.send_template(event=event,gym_info=gym_info)

    def get_image_uri(self, event, r):
        if r.get('photos') is None:
            thurmbnail_image_url = 'https://i.natgeofe.com/n/548467d8-c5f1-4551-9f58-6817a8d2c45e/NationalGeographic_2572187_square.jpg'
        else:
            photo_refernce = r['photos'][0]['photo_reference']
            photo_width = r['photos'][0]['width']
            thurmbnail_image_url = 'https://maps.googleapis.com/maps/api/place/photo?key={}&photoreference={}&maxwidth={}'.format(self.GOOGLE_MAP_API_KEY,photo_refernce,photo_width)
        return thurmbnail_image_url
    
    def get_address(self, event, r):
        dd = "電話:{}\n地址:{}".format(r['formatted_phone_number'],r['formatted_address'])
        return dd
    
    # B.找健身房
    def send_template(self, event, gym_info):
        carousel_template_message = TemplateSendMessage(
            alt_text='地點',
            template=CarouselTemplate(
                columns=[
                        CarouselColumn(
                            thumbnail_image_url= self.get_image_uri(event,r),
                            title=r['name'],
                            text=self.get_address(event,r),
                            actions=[
                                URIAction(
                                    label='Google Map',
                                    uri=r['url']
                                )
                            ]
                        )for r in gym_info
                    ]
                 )
             )
        return carousel_template_message
