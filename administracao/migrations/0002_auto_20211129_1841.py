# Generated by Django 3.2.9 on 2021-11-29 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracao', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servico',
            name='porcentagem_comissao',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='servico',
            name='valor_banheiro',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='servico',
            name='valor_cozinha',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='servico',
            name='valor_minimo',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='servico',
            name='valor_outros',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='servico',
            name='valor_quarto',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='servico',
            name='valor_quintal',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='servico',
            name='valor_sala',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
