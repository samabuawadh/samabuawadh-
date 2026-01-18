from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window

Window.clearcolor = (0.95, 0.95, 0.95, 1)

class TaxCalculatorApp(App):
    def build(self):
        self.title = 'حاسبة الضرائب المتطورة'

        # Layout رئيسي
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # عنوان التطبيق
        title = Label(
            text='حاسبة الضرائب المتطورة',
            size_hint=(1, 0.1),
            font_size='20sp',
            bold=True,
            color=(0.2, 0.2, 0.2, 1)
        )
        main_layout.add_widget(title)

        # حقول الإدخال
        fields_layout = BoxLayout(orientation='vertical', spacing=5, size_hint=(1, 0.4))

        self.entry1 = self.create_field(fields_layout, 'المبلغ قبل الضريبة:')
        self.entry2 = self.create_field(fields_layout, 'قيمة الضريبة:')
        self.entry3 = self.create_field(fields_layout, 'نسبة الضريبة (%):')
        self.entry4 = self.create_field(fields_layout, 'المبلغ بعد الضريبة:')

        main_layout.add_widget(fields_layout)

        # الأزرار
        buttons_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.1))

        calc_btn = Button(
            text='احسب الآن',
            background_color=(0.18, 0.8, 0.44, 1),
            bold=True,
            font_size='16sp'
        )
        calc_btn.bind(on_press=self.calculate)

        clear_btn = Button(
            text='مسح الكل',
            background_color=(0.91, 0.3, 0.24, 1),
            bold=True,
            font_size='16sp'
        )
        clear_btn.bind(on_press=self.clear_all)

        buttons_layout.add_widget(calc_btn)
        buttons_layout.add_widget(clear_btn)
        main_layout.add_widget(buttons_layout)

        # قسم النتائج
        results_title = Label(
            text='ملخص الحساب',
            size_hint=(1, 0.08),
            font_size='18sp',
            bold=True,
            color=(0.2, 0.2, 0.2, 1)
        )
        main_layout.add_widget(results_title)

        results_layout = GridLayout(cols=2, spacing=10, size_hint=(1, 0.25))

        self.res_v1 = self.create_result(results_layout, 'قبل الضريبة:', '0.000')
        self.res_v2 = self.create_result(results_layout, 'قيمة الضريبة:', '0.000')
        self.res_v3 = self.create_result(results_layout, 'نسبة الضريبة:', '0.000%')
        self.res_total = self.create_result(results_layout, 'المبلغ الإجمالي:', '0.000', is_total=True)

        main_layout.add_widget(results_layout)

        # حقوق الملكية
        copyright_label = Label(
            text='حقوق الملكية: سامر عوض - التدقيق الداخلي',
            size_hint=(1, 0.07),
            font_size='12sp',
            italic=True,
            color=(0.4, 0.4, 0.4, 1)
        )
        main_layout.add_widget(copyright_label)

        return main_layout

    def create_field(self, parent, label_text):
        field_box = BoxLayout(orientation='horizontal', spacing=5, size_hint=(1, None), height=40)

        label = Label(
            text=label_text,
            size_hint=(0.5, 1),
            font_size='14sp',
            color=(0.2, 0.2, 0.2, 1),
            halign='right',
            valign='middle'
        )
        label.bind(size=label.setter('text_size'))

        text_input = TextInput(
            multiline=False,
            input_filter='float',
            size_hint=(0.5, 1),
            font_size='14sp',
            halign='center'
        )

        field_box.add_widget(label)
        field_box.add_widget(text_input)
        parent.add_widget(field_box)

        return text_input

    def create_result(self, parent, label_text, default_value, is_total=False):
        label = Label(
            text=label_text,
            font_size='14sp',
            color=(0.2, 0.2, 0.2, 1),
            halign='right',
            valign='middle'
        )
        label.bind(size=label.setter('text_size'))

        value_label = Label(
            text=default_value,
            font_size='16sp' if is_total else '14sp',
            bold=True,
            color=(0, 0, 1, 1) if is_total else (0.2, 0.2, 0.2, 1),
            halign='left',
            valign='middle'
        )
        value_label.bind(size=value_label.setter('text_size'))

        parent.add_widget(label)
        parent.add_widget(value_label)

        return value_label

    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message, halign='center'),
            size_hint=(0.8, 0.3)
        )
        popup.open()

    def calculate(self, instance):
        try:
            vals = {
                'before': self.entry1.text,
                'tax_val': self.entry2.text,
                'rate': self.entry3.text,
                'after': self.entry4.text
            }

            v = {k: float(val) if val else None for k, val in vals.items()}
            known_keys = [k for k, val in v.items() if val is not None]

            if len(known_keys) < 2:
                self.show_popup('تنبيه', 'يرجى إدخال قيمتين على الأقل للحساب')
                return

            # منطق الحساب الشامل
            if v['before'] is not None:
                if v['rate'] is not None:
                    v['tax_val'] = v['before'] * (v['rate'] / 100)
                    v['after'] = v['before'] + v['tax_val']
                elif v['tax_val'] is not None:
                    v['after'] = v['before'] + v['tax_val']
                    v['rate'] = (v['tax_val'] / v['before']) * 100 if v['before'] != 0 else 0
                elif v['after'] is not None:
                    v['tax_val'] = v['after'] - v['before']
                    v['rate'] = (v['tax_val'] / v['before']) * 100 if v['before'] != 0 else 0

            elif v['after'] is not None:
                if v['rate'] is not None:
                    v['before'] = v['after'] / (1 + (v['rate'] / 100))
                    v['tax_val'] = v['after'] - v['before']
                elif v['tax_val'] is not None:
                    v['before'] = v['after'] - v['tax_val']
                    v['rate'] = (v['tax_val'] / v['before']) * 100 if v['before'] != 0 else 0

            elif v['tax_val'] is not None and v['rate'] is not None:
                v['before'] = v['tax_val'] / (v['rate'] / 100)
                v['after'] = v['before'] + v['tax_val']

            # تحديث النتائج
            self.res_v1.text = f"{v['before']:.3f}"
            self.res_v2.text = f"{v['tax_val']:.3f}"
            self.res_v3.text = f"{v['rate']:.3f}%"
            self.res_total.text = f"{v['after']:.3f}"

        except Exception as e:
            self.show_popup('خطأ', 'تأكد من إدخال أرقام صحيحة')

    def clear_all(self, instance):
        self.entry1.text = ''
        self.entry2.text = ''
        self.entry3.text = ''
        self.entry4.text = ''
        self.res_v1.text = '0.000'
        self.res_v2.text = '0.000'
        self.res_v3.text = '0.000%'
        self.res_total.text = '0.000'

if __name__ == '__main__':
    TaxCalculatorApp().run()
