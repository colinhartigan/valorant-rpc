import psutil
import os

class Processes:

    @staticmethod
    def are_processes_running(required_processes=["VALORANT-Win64-Shipping.exe", "RiotClientServices.exe"]):
        processes = []
        for proc in psutil.process_iter():
            processes.append(proc.name())
        
        return set(required_processes).issubset(processes)

    @staticmethod
    def is_program_already_running():
        processes = []
        for proc in psutil.process_iter():
            processes.append(proc.name())

        if len([proc for proc in processes if proc == "valorant-rpc.exe"]) > 2:
            return True

        return False