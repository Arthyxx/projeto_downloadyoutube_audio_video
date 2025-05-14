import flet as ft
from pytube import YouTube

class YoutubeDownloaderApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Youtube Downloader"
        self.page.window_width = 500
        self.page.window_height = 250
        self.page.window_resizable = False

        self.link_input = ft.TextField(label="Link do Youtube", width=400)
        self.status_text = ft.Text("", color="blue")

        self.build()

    def build(self):
        self.page.add(
            ft.Column([
                self.link_input,
                ft.Row([
                    ft.ElevatedButton("Baixar Vídeo", on_click=self.baixar_video),
                    ft.ElevatedButton("Baixar Áudio", on_click=self.baixar_audio),
                ], spacing=20),
                self.status_text
            ], spacing=20, alignment="center")
        )
    
    def baixar_video(self, e):
        link = self.link_input.value.strip()
        if not link:
            self.status_text.value = "Por favor, insira um link válido."
            self.status_text.color = "red"
            self.page.update()
            return
        
        try:
            yt = YouTube(link)
            stream = yt.streams.get_highest_resolution()
            self.status_text.value = "Baixando vídeo..."
            self.page.update()
            
            stream.download()
            self.status_text.value = "Vídeo baixado com sucesso!"
            self.status_text.color = "green"
        except Exception as ex:
            self.status_text.value = f"Erro: {str(ex)}"
            self.status_text.color = "red"

        self.page.update()    
    
    
    def baixar_audio(self, e):
        self.status_text.value = "Baixando áudio..."
        self.page.update()

def main(page: ft.Page):
    YoutubeDownloaderApp(page)

ft.app(target=main)
