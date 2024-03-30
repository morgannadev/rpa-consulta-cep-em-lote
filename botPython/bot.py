from botcity.web import WebBot, Browser, By, table_to_dict
from botcity.maestro import *

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False

LINK_CONSULTA_CEP_CORREIOS = "https://buscacepinter.correios.com.br/app/endereco/index.php"

def main():
    maestro = BotMaestroSDK.from_sys_args()
    execution = maestro.get_execution()

    # Obtendo o CEP a ser consultado via parâmetro da tarefa
    cep = execution.parameters.get("cep")

    bot = WebBot()
    bot.headless = False
    bot.browser = Browser.FIREFOX
    bot.driver_path = r"resources\geckodriver.exe"

    try:
        maestro.alert(
            task_id=execution.task_id,
            title="Iniciando a tarefa",
            message=f"Iniciando a tarefa de consulta do CEP {cep} nos Correios",
            alert_type=AlertType.INFO
        )

        bot.browse(LINK_CONSULTA_CEP_CORREIOS)

        campo_endereco = bot.find_element("endereco", By.ID)
        campo_endereco.send_keys(cep)

        botao_pesquisar = bot.find_element("btn_pesquisar", By.ID)
        botao_pesquisar.click()

        tabela_enderecos = bot.find_element("resultado-DNEC", By.ID)
        tabela_enderecos = table_to_dict(tabela_enderecos)[0]

        print(tabela_enderecos)

        bot.wait(100)

        # Registrando log
        maestro.new_log_entry(
            activity_label="consulta-cep-correios",
            values={
                "cep": cep,
                "logradouro": tabela_enderecos["logradouronome"],
                "bairro": tabela_enderecos["bairrodistrito"],
                "localidade": tabela_enderecos["localidadeuf"]
            }
        )      

        # Finalizando tarefa
        maestro.finish_task(
            task_id=execution.task_id,
            status=AutomationTaskFinishStatus.SUCCESS,
            message="Task finalizada com sucesso!"
        )
        
    except Exception as erro:
        bot.save_screenshot("erro.png")

        # Registrando erro
        maestro.error(
            task_id=execution.task_id,
            exception=erro,
            screenshot="erro.png"
        )

        # Finalizando tarefa
        maestro.finish_task(
            task_id=execution.task_id,
            status=AutomationTaskFinishStatus.FAILED,
            message="Task finalizada com erro!"
        )

    finally:
        bot.stop_browser()


if __name__ == '__main__':
    main()
