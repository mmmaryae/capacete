# monta o dado (JSON) que vai pro frontend

def montar_resposta_front(status, tempo=0, alerta=False, imagem=None):
    return {
        "scanner_ativo": True,
        "status": status,
        "tempo_sem_capacete": round(tempo, 1),
        "alerta": alerta,
        "mensagem": "ALERTA: pessoa sem capacete" if alerta else "Monitorando",
        "imagem": imagem,
        "acao_front": {
            "tela_vermelha": alerta,
            "tocar_som": alerta
        }
    }