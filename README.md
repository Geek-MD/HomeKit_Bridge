# HomeKit Child Bridge

Integración personalizada para Home Assistant que publica grupos de entidades como
puentes independientes de Apple Home. Cada entrada crea una entrada nativa de
`homekit`, por lo que Home Assistant muestra para ella su propio código QR y código
de emparejamiento.

## Funciones

- Exportación de todas las entidades de un dominio (`light`, `cover`, etc.).
- Exportación de las entidades pertenecientes a una integración configurada.
- Un puente HomeKit independiente por cada selección.
- Eliminación automática del puente administrado cuando se elimina su grupo.
- Sin servidor HAP alternativo: se reutiliza la integración HomeKit incluida en
  Home Assistant.

La integración declara en su manifiesto que reemplaza la configuración directa de
la integración base `homekit`. Internamente continúa utilizando su implementación
HAP nativa para conservar la compatibilidad con Home Assistant y Apple Home.

Consulta [CHANGELOG.md](CHANGELOG.md) para conocer los cambios de cada versión.

## Instalación

1. Copia `custom_components/homekit_child_bridge` a la carpeta
   `custom_components` de Home Assistant.
2. Reinicia Home Assistant.
3. Ve a **Ajustes → Dispositivos y servicios → Añadir integración** y busca
   **HomeKit Child Bridge**.
4. Elige si deseas agrupar por dominio o por integración y selecciona el grupo.
5. Abre la nueva entrada **HomeKit Bridge** creada por Home Assistant para ver y
   escanear su código QR.

> No configures las mismas entidades en varios puentes HomeKit: Apple Home las
> mostrará duplicadas.

## Desarrollo

```bash
python -m pip install -e '.[test]'
pytest
ruff check .
```

## Licencia

MIT
