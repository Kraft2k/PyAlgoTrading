import flet as ft
import sys
from flet import icons

def login_wnd(page: ft.Page):
        page.window_center()
        page.title = "Login"
        page.theme_mode = 'DARK'
        
        page.window_width = 560
        page.window_height = 490
        
        page.window_resizable = False
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        
        def handle_submit(e):
            page.window_close()

        def register(e):
            #print(">>")
            #print(user_login.value)
            #print(user_password.value)
            page.window_close()
            
        def validate(e):
            if all([user_login.value,user_password.value]):
                btn_reg.disabled = False
            else:
                btn_reg.disabled = True
            page.update()   
        
        user_login = ft.TextField(
            label='Username',
            width=320,
            height=45,
            border_color='grey',
            prefix_icon=ft.icons.PEOPLE,
            on_submit=handle_submit,
            on_change=validate
        )
        user_password = ft.TextField(
            label='Password',
            width=320, 
            height=45, 
            border_color='grey',
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.icons.KEY,
            on_submit=handle_submit,
            on_change=validate
        )
        btn_reg = ft.OutlinedButton(text='Log in', width=320, height=45, on_click=register,disabled=True)

        page.add(
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text('Axioma Workstation', size=27, color="WHITE"),
                            ft.Text('Live Trading', size=13, color="LIME"),
                            user_login,
                            user_password,
                            ft.Text('                                                                 Need Help?', size=13, height=33, color="grey"),
                            #ft.Text('Need Help?', text_align=ft.TextAlign.RIGHT, height=33),
                            btn_reg,
                            ft.Text('', height=1),
                            ft.Text('No username? Try the demo', size=13, color="blue")

                        ]
                    )
                 ],
                 alignment=ft.MainAxisAlignment.CENTER
            ) 
        )
        
             
        page.update()
    
ft.app(target=login_wnd)

