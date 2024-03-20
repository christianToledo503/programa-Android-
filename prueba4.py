from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import NumericProperty
from kivy.animation import Animation


class DismissibleBoxLayout(ButtonBehavior, BoxLayout):
    swipe_threshold = NumericProperty(100)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            self.start_x = touch.x
            self.start_y = touch.y
            self.org_x = self.x
            return True
        return super(DismissibleBoxLayout, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            dx = touch.x - self.start_x
            dy = touch.y - self.start_y
            if abs(dy) < 20 and dx > 0:
                self.x = self.org_x + dx
                return True
        return super(DismissibleBoxLayout, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            dx = touch.x - self.start_x
            dy = touch.y - self.start_y
            if dx > self.swipe_threshold:
                self.dismiss()
            else:
                anim = Animation(x=self.org_x, duration=0.2)
                anim.start(self)
            touch.ungrab(self)
            return True
        return super(DismissibleBoxLayout, self).on_touch_up(touch)

    def dismiss(self):
        parent = self.parent
        anim = Animation(opacity=0, x=self.parent.width, duration=0.5)
        anim.bind(on_complete=lambda *args: parent.remove_widget(self))
        anim.start(self)


class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        
        self.cols = 1

        for i in range(20):
            box_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)

            label = Label(text=f"Item {i}", size_hint_x=0.7)
            image = Image(source="logo.png", size_hint_x=0.3)

            box_layout.add_widget(label)
            box_layout.add_widget(image)

            dismissible_box = DismissibleBoxLayout(orientation='horizontal', size_hint=(None, None), size=(self.width, 50))
            dismissible_box.add_widget(box_layout)

            self.add_widget(dismissible_box)


class MyApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()
