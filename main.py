import flet as ft
import subprocess

class YouTubeDownloaderApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "YouTube Downloader"
        self.page.window_width = 800
        self.page.window_height = 600
        self.page.window_resizable = False
        self.page.update()

        self.page.padding = 10

        # Inputs e botões
        self.link_input = ft.TextField(label="Link do YouTube", width=400)
        self.output_folder = ft.TextField(label="Pasta de destino", read_only=True, width=400)
        self.select_folder_button = ft.ElevatedButton("Selecionar Pasta", on_click=self.selecionar_pasta)
        self.status_text = ft.Text("", color="blue")
        self.loader = ft.ProgressRing(visible=False)

        self.build()

    def selecionar_pasta(self, e):
        def on_result(e: ft.FilePickerResultEvent):
            if e.path:
                self.output_folder.value = e.path
                self.page.update()

        file_picker = ft.FilePicker(on_result=on_result)
        self.page.overlay.append(file_picker)
        self.page.update()
        file_picker.get_directory_path()

    def build(self):
        self.page.add(
            ft.Column([ 
                ft.Row([self.link_input], alignment="center"),
                ft.Row([self.output_folder, self.select_folder_button], spacing=10, alignment="center"),
                ft.Row([ft.ElevatedButton("Baixar Vídeo", on_click=self.baixar_video),
                        ft.ElevatedButton("Baixar Áudio", on_click=self.baixar_audio)], spacing=10, alignment="center"),
                ft.Row([self.loader], alignment="center"),
                ft.Row([self.status_text], alignment="center")
            ], spacing=20, alignment="center", expand=True)
        )

    def baixar_video(self, e):
        link = self.link_input.value.strip()
        if not link:
            self.status_text.value = "Por favor, insira um link válido."
            self.status_text.color = "red"
            self.page.update()
            return

        pasta_destino = self.output_folder.value.strip()
        if not pasta_destino:
            self.status_text.value = "Por favor, selecione uma pasta de destino."
            self.status_text.color = "red"
            self.page.update()
            return

        try:
            self.status_text.value = "Baixando vídeo..."
            self.status_text.color = "blue"
            self.page.update()

            self.loader.visible = True
            self.page.update()

            self.link_input.disabled = True
            self.select_folder_button.disabled = True
            self.page.update()

            subprocess.run([
                "yt-dlp",
                "-f", "best",
                "-o", f"{pasta_destino}/%(title)s.%(ext)s",
                link
            ])

            self.status_text.value = "Vídeo baixado com sucesso!"
            self.status_text.color = "green"

        except Exception as ex:
            self.status_text.value = f"Erro: {str(ex)}"
            self.status_text.color = "red"

        finally:
            self.loader.visible = False
            self.link_input.disabled = False
            self.select_folder_button.disabled = False
            self.page.update()

    def baixar_audio(self, e):
        link = self.link_input.value.strip()
        if not link:
            self.status_text.value = "Por favor, insira um link válido"
            self.status_text.color = "red"
            self.page.update()
            return

        pasta_destino = self.output_folder.value.strip()
        if not pasta_destino:
            self.status_text.value = "Por favor, selecione uma pasta destino."
            self.status_text.color = "red"
            return

        try:
            self.status_text.value = "Baixando áudio..."
            self.status_text.color = "blue"
            self.page.update()

            self.loader.visible = True
            self.page.update()

            self.link_input.disabled = True
            self.select_folder_button.disabled = True
            self.page.update()

            subprocess.run([
                "yt-dlp",
                "-x",
                "--audio-format", "mp3",
                "-o", f"{pasta_destino}/%(title)s.%(ext)s",
                link
            ])

            self.status_text.value = "Áudio baixado com sucesso!"
            self.status_text.color = "green"

        except Exception as ex:
            self.status_text.value = f"Erro: {str(ex)}"
            self.status_text.color = "red"

        finally:
            self.loader.visible = False
            self.link_input.disabled = False
            self.select_folder_button.disabled = False
            self.page.update()

def main(page: ft.Page):
    page.window_width = 800
    page.window_height = 600
    page.window_resizable = False
    page.update()
    page.title = "Youtube Downloader"
    YouTubeDownloaderApp(page)

ft.app(target=main)
