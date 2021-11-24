import os
import imghdr
from requests_toolbelt.multipart.encoder import MultipartEncoder

from kivymd.app import MDApp
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import ButtonBehavior

from kivy.utils import platform
from kivy.metrics import dp
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.network.urlrequest import UrlRequest
from kivy.graphics import Color, RoundedRectangle

from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.toolbar import MDToolbar
from kivymd.toast import toast
from kivymd.uix.behaviors import (
    RectangularElevationBehavior,
    CircularRippleBehavior,
    
)

from plyer import storagepath


if platform == 'android':
    from android.permissions import request_permissions, check_permission, Permission

API_URL = 'http://192.168.1.11:8000/predict'


class FullImage(Image): pass
class PredictionImage(Image): pass

class UploadFileCard(
    ButtonBehavior,
    BoxLayout): 
    pass

class LoadingCard(
    ButtonBehavior,
    BoxLayout): 
    pass

class PredictionCard(
    RectangularElevationBehavior,
    ButtonBehavior,
    BoxLayout):
    image_source = StringProperty('./assets/background.jpg')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ClearCard(
    RectangularElevationBehavior,
    CircularRippleBehavior,
    ButtonBehavior,
    BoxLayout): 
    pass

class MainLayout(FloatLayout): pass

class PredictionApp(MDApp):
    FILE_HAS_SELECTED = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = 'DeepOrange'
        self.theme_cls.primary_hue = '900'
        Window.bind(on_keyboard=self.events)

        self.selected_file = None

        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            previous=True,
        )
        self.manager_open = False

    def build(self):
        Builder.load_file('main.kv')

        self.upload_file_card = UploadFileCard(
            pos_hint={'center_y': .5, 'center_x': .5},
            size_hint=(None, None),
            size=(Window.width*.9, Window.width*.9),
        )

        self.prediction_card = PredictionCard(
            pos_hint={'top': .85, 'center_x': .5},
            size_hint=(None, None),
            size=(Window.width*.9, Window.height*.62)
        )

        self.loading_card = LoadingCard(
            pos_hint={'center_y': .5, 'center_x': .5},
            size_hint=(None, None),
            size=(Window.width*.9, Window.width*.9),
        )

        self.clear_btn = ClearCard(
            pos_hint={'top': .18, 'center_x': .5},
            size_hint=(None, None),
            size=(Window.width*.9, Window.height*.1)
        )

       
        self.mui = MainLayout()

        self.mui.add_widget(FullImage(
                source='assets/background.jpg',
                pos_hint={'top': 1, 'center_x': .5},
                size_hint=(1,1)
            ),
        )
        
        self.mui.add_widget(MDToolbar(
            title='Tomato Disease Prediction',
            pos_hint={'top': 1},
            elevation=0))

            
        self.mui.add_widget(self.upload_file_card)
        return self.mui

    def on_start(self):
        self.clear_btn.bind(on_press=lambda e: self.clearPrediction())
        self.upload_file_card.bind(on_press=lambda e: self.open_file_manager())

        if platform == 'android':
            has_perms = check_permission('android.permission.READ_EXTERNAL_STORAGE')
            if not has_perms:
                request_permissions([
                    Permission.WRITE_EXTERNAL_STORAGE, 
                    Permission.READ_EXTERNAL_STORAGE]
                )
        
        return super().on_start()

    def clearPrediction(self):
        self.mui.remove_widget(self.prediction_card)
        self.mui.remove_widget(self.clear_btn)
        self.mui.add_widget(self.upload_file_card)

    def open_file_manager(self):
        if platform == 'android':
            has_perms = check_permission('android.permission.READ_EXTERNAL_STORAGE')
            if not has_perms:
                request_permissions([
                    Permission.WRITE_EXTERNAL_STORAGE, 
                    Permission.READ_EXTERNAL_STORAGE]
                )

        self.file_manager.show(storagepath.get_pictures_dir())
        self.manager_open = True

    def send_file(self, file):

        self.mui.add_widget(self.loading_card)

        with open(file, 'rb') as f:
            image_data = f.read()

        image_type = imghdr.what(None, h=image_data)
        mime_type = f'image/{image_type}'

        payload = MultipartEncoder(
            fields={
                'file': (
                    file,
                    image_data,
                    mime_type,
                )
            }
        )

        headers = {
            'accept': 'application/json',
            'Content-Type': payload.content_type
        }

        self.req = UrlRequest(API_URL, req_body=payload, req_headers=headers,
            on_progress=self.on_request_progress,
            on_success=self.on_request_success,
            on_error=self.on_request_failure,
            on_cancel=self.on_request_failure,
            on_failure=self.on_request_failure,
            on_redirect=self.on_request_failure,
            )


    def select_path(self, path):
        
        self.exit_manager()
        self.FILE_HAS_SELECTED = True
        self.selected_file = path

        if not os.path.isfile(self.selected_file):
            toast('Invalid Image Path')
            return

        self.send_file(self.selected_file)
        

    def on_request_success(self, request, result):
        self.prediction_card.ids['prediction_image'].source = self.selected_file

        self.mui.remove_widget(self.loading_card)
        self.mui.remove_widget(self.upload_file_card)
        self.mui.add_widget(self.prediction_card)
        self.mui.add_widget(self.clear_btn)

        self.prediction_card.ids['disease_class'].text = result['class']
        self.prediction_card.ids['confidance'].text = str(round(result['confidance']*100, 2))+"%"

        self.loading_card.ids['loading'].text = 'Loading...'

    def on_request_progress(self, request, result, *a):
        loading = self.loading_card.ids['loading']
        loading.text = loading.text + '.'

    def on_request_failure(self, *a):
        self.mui.remove_widget(self.loading_card)
        self.prediction_card.ids['disease_class'].text = ''
        self.prediction_card.ids['confidance'].text = ''
        self.loading_card.ids['loading'].text = 'Loading...'

        toast('Error has occured, please try again')


    def exit_manager(self, *args):
        self.FILE_HAS_SELECTED = False
        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
       
        if keyboard in (1001, 27):
            if self.manager_open:
                print('file open')
                self.file_manager.back()
        return False


if __name__ == '__main__':
    PredictionApp().run()
