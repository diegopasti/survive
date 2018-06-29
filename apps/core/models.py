from django.db import models

# Create your models here.


class Character(models.Model):

    strength = models.DecimalField("Força", max_digits=5, decimal_places=2)
    agility = models.DecimalField("Agilidade", max_digits=5, decimal_places=2)
    resistance = models.DecimalField("Resistência", max_digits=5, decimal_places=2)
    hability = models.DecimalField("Habilidade", max_digits=5, decimal_places=2)
    luck = models.DecimalField("Sorte", max_digits=5, decimal_places=2)
    health = models.DecimalField("Vida", max_digits=5, decimal_places=3)
    energy = models.DecimalField("Mana", max_digits=5, decimal_places=2)
    damage = models.DecimalField("Dano", max_digits=5, decimal_places=2)
    defense = models.DecimalField("Defesa", max_digits=5, decimal_places=2)
    attack_speed = models.DecimalField("Velocidade de Ataque", max_digits=5, decimal_places=2)
    move_speed = models.DecimalField("Velocidade de Movimento", max_digits=5, decimal_places=2)
    field_of_view = models.DecimalField("Visão", max_digits=5, decimal_places=2)
    #critical_damage = models.DecimalField("", max_digits=5, decimal_places=2)
    critical_chance = models.DecimalField("Taxa Crítico", max_digits=5, decimal_places=2)
    health_regen = models.DecimalField("Regeneração de Vida", max_digits=5, decimal_places=2)
    energy_regen = models.DecimalField("Regeneração de Mana", max_digits=5, decimal_places=2)




