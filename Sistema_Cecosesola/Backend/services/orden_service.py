import json
from database.db import get_db_connection

class OrdenService:
    @staticmethod
    def crear_orden_completa(data):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # 1. Crear la Orden (Autorizada automáticamente por el pago)
            cursor.execute("""
                INSERT INTO ordenes (cedula_paci, id_medico_tratante, estado, autorizado)
                VALUES (?, ?, 'En Espera', 1) RETURNING id_orden;
            """, (data.cedula_paci, data.id_medico_tratante))
            id_orden = cursor.fetchone()[0]

            # 2. Insertar cada estudio médico en los Detalles
            for servicio in data.servicios:
                cursor.execute("""
                    INSERT INTO orden_detalles (id_orden, id_servicio, estado_examen)
                    VALUES (?, ?, 'Pendiente');
                """, (id_orden, servicio.id_servicio))

            # 3. Emitir el Documento de Facturación
            cursor.execute("""
                INSERT INTO documentos_facturacion 
                (id_orden, cedula_paci, tipo_documento, razon_social, subtotal, iva, monto_total, estado_pago, id_cajero)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'Pagado', ?) RETURNING id_documento;
            """, (id_orden, data.cedula_paci, data.tipo_documento, data.razon_social, 
                  data.subtotal, data.iva, data.monto_total, data.id_cajero))
            id_documento = cursor.fetchone()[0]

            # 4. Registrar el Pago Recibido
            cursor.execute("""
                INSERT INTO pagos_recibidos (id_documento, metodo_pago, monto_pagado, referencia)
                VALUES (?, ?, ?, ?);
            """, (id_documento, data.metodo_pago, data.monto_total, data.referencia))

            conn.commit()
            return {"mensaje": "Orden clínica y facturación procesadas con éxito", "id_orden": id_orden}
        
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def obtener_lista_espera():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT od.id_detalle, o.id_orden, p.nombre_completo, c.descripcion AS examen, od.estado_examen
            FROM orden_detalles od
            JOIN ordenes o ON od.id_orden = o.id_orden
            JOIN pacientes p ON o.cedula_paci = p.cedula_paci
            JOIN catalogo_servicio c ON od.id_servicio = c.id_servicio
            WHERE o.autorizado = 1 AND od.estado_examen = 'Pendiente'
            ORDER BY o.fecha_creacion ASC;
        """)
        ordenes = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return ordenes

    @staticmethod
    def cargar_resultados_json(id_detalle: int, data):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE orden_detalles 
                SET id_usuario_procesa = ?,
                    datos_laboratorio = ?,
                    estado_examen = ?
                WHERE id_detalle = ? RETURNING id_detalle;
            """, (data.id_usuario_procesa, json.dumps(data.datos_laboratorio), data.estado_examen, id_detalle))
            
            actualizado = cursor.fetchone()
            conn.commit()
            return dict(actualizado) if actualizado else None
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()