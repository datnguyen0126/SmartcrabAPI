from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re, random

from api_result.models import ClusteringScores
from api_data.models import CpuScore, GpuScore, Laptop


class ClusterServices:

    @classmethod
    def set_score_gpu(cls, item):
        gpu_scores = GpuScore.objects.all()
        max_ratio = 0
        detected_gpu = None
        if not item.vga or item.vga == 'Onboard':
            item.vga = 'Intel UHD graphics'
            item.save()
        for gpu_score in gpu_scores:
            gpu_score_name = gpu_score.name.split('@')[0].replace('Integrated', '')
            item_gpu = re.split('\+|Graph|/', item.vga)[0].replace('GT ', 'GT')
            temp = fuzz.partial_ratio(gpu_score_name.lower(), item_gpu.lower())
            if temp > max_ratio:
                max_ratio = temp
                detected_gpu = gpu_score
        #print(item.vga, ' | ', detected_gpu.name, ' | ', max_ratio)
        if detected_gpu is not None:
            print(detected_gpu.name)
            laptop_score = ClusteringScores.objects.filter(laptop=item).first()
            if laptop_score:
                ClusteringScores.objects.filter(laptop=item).update(laptop_gpu=item.vga, detected_gpu=detected_gpu.name,
                                            detected_gpu_score=detected_gpu.score, gpu_score=detected_gpu)
            else:
                ClusteringScores.objects.create(laptop=item, laptop_gpu=item.vga, detected_gpu=detected_gpu.name,
                                            detected_gpu_score=detected_gpu.score, gpu_score=detected_gpu)


    @classmethod
    def set_score_cpu(cls, item):
        cpu_scores = CpuScore.objects.all()
        max_ratio = 0
        detected_cpu = None
        for cpu_score in cpu_scores:
            cpu_score_name = cpu_score.name.split('@')[0]
            item_cpu = re.split('\(|ghz|Ghz|\.', item.cpu)[0]
            temp = fuzz.ratio(cpu_score_name, item_cpu)
            if temp > max_ratio:
                max_ratio = temp
                detected_cpu = cpu_score
        if detected_cpu is not None:
            laptop_score = ClusteringScores.objects.filter(laptop=item).first()
            if laptop_score:
                laptop_score.laptop_cpu=item.cpu
                laptop_score.detected_cpu=detected_cpu.name
                laptop_score.detected_cpu_score=detected_cpu.score
                laptop_score.cpu_score=detected_cpu
                laptop_score.save()
                return laptop_score
            else:
                return ClusteringScores.objects.create(laptop=item, laptop_cpu=item.cpu, detected_cpu=detected_cpu.name,
                                        detected_cpu_score=detected_cpu.score, cpu_score=detected_cpu)

    @classmethod
    def set_scores(cls):
        ClusteringScores.objects.filter(id__lt=0).delete()
        laptops = Laptop.objects.all()
        for laptop in laptops:
            cls.set_score_cpu(laptop)
            cls.set_score_gpu(laptop)


            



