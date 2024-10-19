import tkinter as tk
from tkinter import filedialog, messagebox
import os
from PyPDF2 import PdfMerger

# Buscar os arquivos na pasta
def buscar_pdf():
    global pdf_paths, pdf_nomes
    pasta = filedialog.askdirectory(title="Selecionar a pasta")
    if pasta:
        # Lista os PDFs na pasta e cria uma lista com os caminhos completos e os nomes
        pdf_paths = sorted([os.path.join(pasta, f) for f in os.listdir(pasta) if f.endswith('.pdf')])
        pdf_nomes = [os.path.basename(f).replace('.pdf', '') for f in pdf_paths]  # Nomes dos arquivos sem extensão

# Combinar os PDFs
def combinar_pdf():
    try:
        # Pegar a ordem inserida na caixa de texto
        ordem = text_area.get("1.0", tk.END).strip().splitlines()  # Pega todas as linhas
        ordem = [nome.strip() for nome in ordem if nome.strip()]  # Remove espaços em branco e linhas vazias

        # Verificar se todos os PDFs da ordem existem na pasta
        faltando = [nome for nome in ordem if nome not in pdf_nomes]
        if faltando:
            messagebox.showerror("Erro", f"Os seguintes PDFs estão faltando: {', '.join(faltando)}")
            return

        # Criar um objeto
        merger = PdfMerger()

        # Adicionar os PDFs na ordem correta
        for nome in ordem:
            index = pdf_nomes.index(nome)
            merger.append(pdf_paths[index])

        # Escolher a pasta e o nome para salvar o novo PDF
        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Arquivos PDF", "*.pdf")])
        if output_path:
            merger.write(output_path)
            merger.close()
            messagebox.showinfo("Sucesso", "PDFs combinados com sucesso!")

        # Limpar a área de texto
        text_area.delete("1.0", tk.END)  # Limpa todo o texto na área

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Fechar a aplicação
def cancelar():
    root.destroy()  # Encerra a aplicação


# Estilizar os botões
def criar_botao_sombreado(master, text, command):
    frame = tk.Frame(master, bg="white", bd=1)
    frame.pack(pady=5)
    btn = tk.Button(frame, text=text, command=command, bg="darkblue", fg="white", relief="flat", padx=10, pady=5, font=("Helvetica", 10, "bold"))
    btn.pack()
    return btn

# Criar a interface gráfica
root = tk.Tk()
root.title("PDF Merge Master")

# Definir a cor de fundo da janela
root.configure(bg="lightblue")

# Estilizar os textos
label = tk.Label(root, text="Insira os files (um por linha):",bg="lightblue", fg="darkblue", font=("Helvetica",12,"bold"))
label.pack(pady=10)

# Área de texto
text_area = tk.Text(root, width=50, height=10, bg="white", fg="black", bd=2, relief="solid", font=("Heveltica",10,"bold"))
text_area.pack(pady=10)

# Botão para buscar os PDFs
criar_botao_sombreado(root, "Buscar PDFs", buscar_pdf)

# Botão para combinar os PDFs
criar_botao_sombreado(root, "Combinar PDFs", combinar_pdf)

# Botão de cancelar
criar_botao_sombreado(root, "Cancelar", cancelar)

# Iniciar a aplicação
root.mainloop()