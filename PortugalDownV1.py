import os
import time
from tkinter import Listbox, Scrollbar, messagebox
from tkinter.ttk import Combobox
from pytube import YouTube
from customtkinter import CTk, CTkLabel, CTkEntry, CTkButton, CTkProgressBar
from tkinter import filedialog

# Lista de qualidades MP3 disponíveis
mp3_qualities = []

# Lista de qualidades MP4 disponíveis
mp4_qualities = []

def preencher_qualidades_mp3(event=None):
    try:
        url = EURL.get()
        yt = YouTube(url)
        audio_streams = yt.streams.filter(only_audio=True, file_extension='mp4')
        global mp3_qualities
        mp3_qualities = [stream.abr for stream in audio_streams if stream.mime_type == 'audio/mp4']

        CQualidadeMp3['values'] = mp3_qualities
        CQualidadeMp3.set(mp3_qualities[0])  # Defina a primeira qualidade como padrão
    except Exception as e:
        Lconclusão.insert("end", f'Erro ao obter as qualidades de áudio MP3: {str(e)}')

def preencher_qualidades_mp4(event=None):
    try:
        url = EURL.get()
        yt = YouTube(url)
        video_streams = yt.streams.filter(progressive=True, file_extension='mp4')
        global mp4_qualities
        mp4_qualities = [f'{stream.resolution} - {stream.fps}' for stream in video_streams]

        CQualidadeMp4['values'] = mp4_qualities
        CQualidadeMp4.set(mp4_qualities[0])  # Defina a primeira qualidade como padrão
    except Exception as e:
        Lconclusão.insert("end", f'Erro ao obter as qualidades de vídeo MP4: {str(e)}')

def download_video():
    url = EURL.get()
    Lconclusão.insert("end", f'Iniciando o download de vídeo da URL: {url}')
    start_time = time.time()  # Registre o tempo de início

    try:
        yt = YouTube(url)
        selected_quality = CQualidadeMp4.get().split(' - ')[0]
        video_stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=selected_quality).first()

        # Obtenha o tamanho total do arquivo em bytes
        file_size = int(video_stream.filesize)

        # Abre uma caixa de diálogo para escolher o local de destino
        dest_folder = filedialog.askdirectory()
        if dest_folder:
            video_stream.download(output_path=dest_folder, filename_prefix='video')

            end_time = time.time()  # Registre o tempo de término
            duration = end_time - start_time
            Lconclusão.insert("end", 'Conclusão Download de Vídeo')
            Lconclusão.insert("end", f'O arquivo foi salvo em: {os.path.join(dest_folder, video_stream.default_filename)}')
            Lconclusão.insert("end", f'Tempo decorrido: {duration:.2f} segundos')
            messagebox.showinfo("Conclusão", "Download de vídeo concluído com sucesso!")

    except Exception as e:
        Lconclusão.insert("end", f'Erro: {str(e)}')
        messagebox.showerror("Erro", f"Ocorreu um erro durante o download: {str(e)}")

def download_audio():
    url = EURL.get()
    Lconclusão.insert("end", f'Iniciando o download de áudio da URL: {url}')
    start_time = time.time()  # Registre o tempo de início

    try:
        yt = YouTube(url)
        audio_streams = yt.streams.filter(only_audio=True, file_extension='mp4')

        selected_quality = CQualidadeMp3.get()

        if selected_quality not in mp3_qualities:
            Lconclusão.insert("end", 'Qualidade não disponível.')
            messagebox.showerror("Erro", "Qualidade de áudio não disponível.")
        else:
            audio_stream = audio_streams.filter(abr=selected_quality).first()

            # Obtenha o tamanho total do arquivo em bytes
            file_size = int(audio_stream.filesize)

            # Abre uma caixa de diálogo para escolher o local de destino
            dest_folder = filedialog.askdirectory()
            if dest_folder:
                audio_stream.download(output_path=dest_folder, filename_prefix='audio')

                end_time = time.time()  # Registre o tempo de término
                duration = end_time - start_time
                Lconclusão.insert("end", f'Conclusão do Download de Áudio: {audio_stream.abr}')
                Lconclusão.insert("end", f'O arquivo de áudio foi salvo em: {os.path.join(dest_folder, audio_stream.default_filename)}')
                Lconclusão.insert("end", f'Tempo decorrido: {duration:.2f} segundos')
                messagebox.showinfo("Conclusão", "Download de áudio concluído com sucesso!")

    except Exception as e:
        Lconclusão.insert("end", f'Erro: {str(e)}')
        messagebox.showerror("Erro", f"Ocorreu um erro durante o download: {str(e)}")

def limpar():
    EURL.delete(0, 'end')
    Lconclusão.delete(0, 'end')
    CQualidadeMp3.set('')
    CQualidadeMp4.set()
   

janela = CTk()
janela.geometry('400x410+100+100')
janela.resizable(width=False, height=False)
janela.title('Ferramenta de Download')

Lautor = CTkLabel(janela, text='© Dev Joel 2023 Portugal Aveiro')
Lautor.place(x=150, y=0)

EURL = CTkEntry(janela, width=370, placeholder_text='insira a URL do youtube')
EURL.place(x=5, y=25)

Lqualidade_Mp3 = CTkLabel(janela, text='MP3')
Lqualidade_Mp3.place(x=5, y=60)
CQualidadeMp3 = Combobox(janela, font=('arial 12'), width=15)
CQualidadeMp3.place(x=45, y=80)

Lqualidade_Mp4 = CTkLabel(janela, text='MP4')
Lqualidade_Mp4.place(x=175, y=60)
CQualidadeMp4 = Combobox(janela, font=('arial 12'), width=15)
CQualidadeMp4.place(x=270, y=80)

BMP4 = CTkButton(janela, text='Download Vídeo', width=40, command=download_video)
BMP4.place(x=10, y=100)

BMP3 = CTkButton(janela, text='Download Áudio', width=40, command=download_audio)
BMP3.place(x=130, y=100)

BLimpar = CTkButton(janela, text='Limpar', width=40, command=limpar)
BLimpar.place(x=250, y=100)

Lconclusão = Listbox(janela, width=53, height=15, font=('arial', 12))
Lconclusão.place(x=5, y=170)

scrollbar = Scrollbar(janela, orient="vertical")
scrollbar.config(command=Lconclusão.yview)
scrollbar.place(x=475, y=170, height=290)
Lconclusão.config(yscrollcommand=scrollbar.set)

# Vincule as funções ao evento de saída de foco da entrada para preencher as qualidades de MP4
EURL.bind("<FocusOut>", preencher_qualidades_mp3)
EURL.bind("<FocusOut>", preencher_qualidades_mp4)

janela.mainloop()
