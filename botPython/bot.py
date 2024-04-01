from botcity.web import WebBot, Browser, By, table_to_dict
from botcity.maestro import *

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False

LINK_CONSULTA_CEP_CORREIOS = "https://buscacepinter.correios.com.br/app/endereco/index.php"

def main():
    maestro = BotMaestroSDK.from_sys_args()
    execution = maestro.get_execution()

    bot = WebBot()
    bot.headless = False
    bot.browser = Browser.FIREFOX
    bot.driver_path = r"resources\geckodriver.exe"
    try:
        datapool = maestro.get_datapool("Datapool_Consulta_CEP_Correios")
        if datapool.is_active():
            while datapool.has_next():
                # adicionar um contador para o insights saber quantos foram processados
                 
                item = datapool.next(task_id=execution.task_id)

                # considerar este trecho principalmente em questão de paralelismo
                if item is None:
                    # item poderia ser 'None', caso outro processo o consumisse antes
                    break

                try:
                    consulta_cep(item, bot, maestro, execution)
                    item.report_done()

                except Exception as erro:
                    # adicionar um contador para o insights saber quantos foram executados com falha

                    item.report_error()

                    bot.save_screenshot("erro.png")

                    # Registrando erro
                    maestro.error(
                        task_id=execution.task_id,
                        exception=erro,
                        screenshot="erro.png",
                        tags={"cep": item["cep"]}
                    )

                    # Registrando arquivo de resultado
                    maestro.post_artifact(
                        task_id=execution.task_id,
                        artifact_name="erro.png",
                        filepath="erro.png"
                    )

        else:
            raise Exception("Datapool inativo.")

        status=AutomationTaskFinishStatus.SUCCESS
        message="Tarefa finalizada com sucesso."

    except Exception as erro:
        bot.save_screenshot("erro.png")

        # Registrando erro
        maestro.error(
            task_id=execution.task_id,
            exception=erro,
            screenshot="erro.png"
        )

        status=AutomationTaskFinishStatus.FAILED
        message="Tarefa finalizada com erro."

    finally:
        bot.stop_browser()

        maestro.finish_task(
            task_id=execution.task_id,
            status=status,
            message=message
        )
    

def consulta_cep(item: DataPoolEntry, bot: WebBot, maestro: BotMaestroSDK, execution: BotExecution):
    
    cep = item["cep"]

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

    bot.save_screenshot("sucesso.png")

    # Registrando arquivo de resultado
    maestro.post_artifact(
        task_id=execution.task_id,
        artifact_name="sucesso.png",
        filepath="sucesso.png"
    )

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

    bot.stop_browser()
    # botao_nova_busca = bot.find_element("btn_nbusca", By.ID)
    # botao_nova_busca.click()

if __name__ == '__main__':
    main()
