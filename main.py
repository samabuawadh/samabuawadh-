import flet as ft

def main(page: ft.Page):
    page.title = "حاسبة الضرائب المتطورة"
    page.padding = 20
    page.rtl = True
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO
    
    # حقول الإدخال
    entry1 = ft.TextField(
        label="المبلغ قبل الضريبة",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
    )
    entry2 = ft.TextField(
        label="قيمة الضريبة",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
    )
    entry3 = ft.TextField(
        label="نسبة الضريبة (%)",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
    )
    entry4 = ft.TextField(
        label="المبلغ بعد الضريبة",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
    )
    
    # النتائج
    res_v1 = ft.Text("0.000", size=16, weight=ft.FontWeight.BOLD)
    res_v2 = ft.Text("0.000", size=16, weight=ft.FontWeight.BOLD)
    res_v3 = ft.Text("0.000%", size=16, weight=ft.FontWeight.BOLD)
    res_total = ft.Text("0.000", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE)
    
    def calculate(e):
        try:
            vals = {
                'before': entry1.value,
                'tax_val': entry2.value,
                'rate': entry3.value,
                'after': entry4.value
            }
            
            v = {k: float(val) if val else None for k, val in vals.items()}
            known_keys = [k for k, val in v.items() if val is not None]
            
            if len(known_keys) < 2:
                page.show_snack_bar(
                    ft.SnackBar(content=ft.Text("يرجى إدخال قيمتين على الأقل للحساب"))
                )
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
            res_v1.value = f"{v['before']:.3f}"
            res_v2.value = f"{v['tax_val']:.3f}"
            res_v3.value = f"{v['rate']:.3f}%"
            res_total.value = f"{v['after']:.3f}"
            page.update()
            
        except Exception:
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text("تأكد من إدخال أرقام صحيحة"))
            )
    
    def clear_all(e):
        entry1.value = ""
        entry2.value = ""
        entry3.value = ""
        entry4.value = ""
        res_v1.value = "0.000"
        res_v2.value = "0.000"
        res_v3.value = "0.000%"
        res_total.value = "0.000"
        page.update()
    
    # بناء الواجهة
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    # العنوان
                    ft.Text(
                        "حاسبة الضرائب المتطورة",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Divider(),
                    
                    # حقول الإدخال
                    entry1,
                    entry2,
                    entry3,
                    entry4,
                    
                    # الأزرار
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "احسب الآن",
                                on_click=calculate,
                                bgcolor=ft.colors.GREEN,
                                color=ft.colors.WHITE,
                                expand=1,
                            ),
                            ft.ElevatedButton(
                                "مسح الكل",
                                on_click=clear_all,
                                bgcolor=ft.colors.RED,
                                color=ft.colors.WHITE,
                                expand=1,
                            ),
                        ],
                        spacing=10,
                    ),
                    
                    ft.Divider(),
                    
                    # ملخص الحساب
                    ft.Text("ملخص الحساب", size=18, weight=ft.FontWeight.BOLD),
                    
                    ft.Row([ft.Text("قبل الضريبة:", size=14), res_v1]),
                    ft.Row([ft.Text("قيمة الضريبة:", size=14), res_v2]),
                    ft.Row([ft.Text("نسبة الضريبة:", size=14), res_v3]),
                    ft.Row([ft.Text("المبلغ الإجمالي:", size=14), res_total]),
                    
                    ft.Divider(),
                    
                    # حقوق الملكية
                    ft.Text(
                        "حقوق الملكية: سامر عوض - التدقيق الداخلي",
                        size=12,
                        italic=True,
                        color=ft.colors.GREY,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                spacing=10,
            ),
            padding=20,
        )
    )

ft.app(target=main)
