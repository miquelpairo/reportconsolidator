"""
Consolidador de informes NIR - Versión 2.0 Híbrida
Combina parsing para resumen ejecutivo + HTML completo embebido
"""
from typing import Dict, Any, Optional
from datetime import datetime


class ReportConsolidatorV2:
    def __init__(self):
        self.baseline_data = None
        self.baseline_html = None
        self.validation_data = None
        self.validation_html = None
        self.predictions_data = None
        self.predictions_html = None
        self.service_info = {}
        
    def add_baseline(self, data: Dict[str, Any], html: str):
        """Añade datos parseados y HTML completo del baseline"""
        self.baseline_data = data
        self.baseline_html = html
        
    def add_validation(self, data: Dict[str, Any], html: str):
        """Añade datos parseados y HTML completo de validación"""
        self.validation_data = data
        self.validation_html = html
        
    def add_predictions(self, data: Dict[str, Any], html: str):
        """Añade datos parseados y HTML completo de predicciones"""
        self.predictions_data = data
        self.predictions_html = html
    
    def set_service_info(self, service_info: Dict[str, str]):
        """Establece la información del servicio (editable por el usuario)"""
        self.service_info = service_info
    
    def generate_html(self) -> str:
        """Genera el HTML del informe consolidado"""
        sensor_id = self.service_info.get('sensor_id', 'N/A')
        fecha_informe = self.service_info.get('fecha', datetime.now().strftime('%Y-%m-%d'))
        
        # Generar resumen ejecutivo
        executive_summary = self._generate_executive_summary()
        
        # Construir índice dinámico
        index_items = self._generate_index()
        
        # Construir secciones colapsables con resumen parseado + iframe
        sections_html = []
        
        if self.baseline_html and self.baseline_data:
            sections_html.append(self._generate_collapsible_section(
                'baseline',
                '📐 Baseline Adjustment',
                self._generate_baseline_summary(),
                self.baseline_html
            ))
        
        if self.validation_html and self.validation_data:
            sections_html.append(self._generate_collapsible_section(
                'validation',
                '✅ Validación Óptica',
                self._generate_validation_summary(),
                self.validation_html
            ))
        
        if self.predictions_html and self.predictions_data:
            sections_html.append(self._generate_collapsible_section(
                'predictions',
                '🔬 Predicciones con Muestras Reales',
                self._generate_predictions_summary(),
                self.predictions_html
            ))
        
        # Ensamblar HTML completo
        html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Informe Consolidado - {sensor_id}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        {self._get_styles()}
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>📋 Índice</h2>
        <ul>
            {index_items}
        </ul>
    </div>
    
    <div class="main-content">
        {self._generate_header()}
        
        {executive_summary}
        
        {''.join(sections_html)}
        
        {self._generate_footer()}
    </div>
</body>
</html>
"""
        return html
    
    def _generate_header(self) -> str:
        """Genera el header con información del servicio"""
        # Construir tabla de información
        info_rows = []
        if self.service_info.get('sensor_id'):
            info_rows.append(f"<tr><td><strong>ID del Sensor</strong></td><td>{self.service_info['sensor_id']}</td></tr>")
        if self.service_info.get('fecha'):
            info_rows.append(f"<tr><td><strong>Fecha del Servicio</strong></td><td>{self.service_info['fecha']}</td></tr>")
        if self.service_info.get('tecnico'):
            info_rows.append(f"<tr><td><strong>Técnico Responsable</strong></td><td>{self.service_info['tecnico']}</td></tr>")
        if self.service_info.get('cliente'):
            info_rows.append(f"<tr><td><strong>Cliente</strong></td><td>{self.service_info['cliente']}</td></tr>")
        if self.service_info.get('ubicacion'):
            info_rows.append(f"<tr><td><strong>Ubicación</strong></td><td>{self.service_info['ubicacion']}</td></tr>")
        if self.service_info.get('modelo'):
            info_rows.append(f"<tr><td><strong>Modelo del Equipo</strong></td><td>{self.service_info['modelo']}</td></tr>")
        
        info_table = ""
        if info_rows:
            info_table = f"""
            <div style="margin-top: 20px;">
                <h3 style="margin-top: 0;">Información del Servicio</h3>
                <table style="width: 100%; margin-top: 15px;">
                    {''.join(info_rows)}
                </table>
            </div>
            """
        
        notas_section = ""
        if self.service_info.get('notas'):
            notas_section = f"""
            <div style="margin-top: 15px; padding: 15px; background-color: #f5f5f5; border-left: 3px solid #64B445; border-radius: 5px;">
                <strong>Notas:</strong> {self.service_info['notas']}
            </div>
            """
        
        return f"""
        <div style="background-color: #f8f9fa; padding: 30px; border-radius: 10px; margin-bottom: 30px; border: 1px solid #ddd;">
            <h1 style="margin: 0; color: #000000;">Informe Consolidado de Mantenimiento Preventivo NIR</h1>
            {info_table}
            {notas_section}
        </div>
        """
    
    def _generate_executive_summary(self) -> str:
        """Genera el resumen ejecutivo usando datos parseados"""
        estado_global = self._determine_global_status()
        
        metrics_cards = []
        
        # Baseline
        if self.baseline_data:
            summary = self.baseline_data.get('summary', {})
            stats = self.baseline_data.get('estadisticas_correccion', {})
            offset = stats.get('Corrección Máxima', 'N/A')
            estado = summary.get('estado_global', 'N/A')
            
            metrics_cards.append(f"""
                <div class="metric-card info">
                    <div class="metric-label">Baseline Adjustment</div>
                    <div class="metric-value-small">{offset}</div>
                    <div class="metric-sublabel">Offset Global | Estado: {estado}</div>
                </div>
            """)
        
        # Validación
        if self.validation_data:
            exec_summary = self.validation_data.get('resumen_ejecutivo', {})
            metricas = exec_summary.get('metricas', {})
            total = metricas.get('Total Estándares', '0')
            validados = metricas.get('Validados', '0')
            revisar = metricas.get('Revisar', '0')
            fallidos = metricas.get('Fallidos', '0')
            
            card_class = 'ok' if fallidos == '0' else 'fail'
            
            metrics_cards.append(f"""
                <div class="metric-card {card_class}">
                    <div class="metric-label">Validación Óptica</div>
                    <div class="metric-value">{validados}/{total}</div>
                    <div class="metric-sublabel">Validados (⚠️{revisar} | ❌{fallidos})</div>
                </div>
            """)
        
        # Predicciones
        if self.predictions_data:
            info = self.predictions_data.get('info_general', {})
            productos = info.get('Productos Analizados', 'N/A')
            lamparas = info.get('Lámparas Comparadas', 'N/A')
            
            metrics_cards.append(f"""
                <div class="metric-card info">
                    <div class="metric-label">Predicciones</div>
                    <div class="metric-value">{productos}</div>
                    <div class="metric-sublabel">Productos ({lamparas} lámparas)</div>
                </div>
            """)
        
        status_class = {
            'OK': 'ok',
            'WARNING': 'warning',
            'FAIL': 'fail',
            'UNKNOWN': 'info'
        }.get(estado_global, 'info')
        
        status_icon = {
            'OK': '✅',
            'WARNING': '⚠️',
            'FAIL': '❌',
            'UNKNOWN': 'ℹ️'
        }.get(estado_global, 'ℹ️')
        
        status_text = {
            'OK': 'VALIDACIÓN EXITOSA',
            'WARNING': 'REVISAR RESULTADOS',
            'FAIL': 'VALIDACIÓN FALLIDA',
            'UNKNOWN': 'ESTADO DESCONOCIDO'
        }.get(estado_global, 'ESTADO DESCONOCIDO')
        
        return f"""
        <div class="info-box" id="resumen-ejecutivo">
            <h2>📊 Resumen Ejecutivo</h2>
            
            <div class="metrics-grid">
                <div class="metric-card total">
                    <div class="metric-value">{len([x for x in [self.baseline_data, self.validation_data, self.predictions_data] if x])}</div>
                    <div class="metric-label">Informes Consolidados</div>
                </div>
                {''.join(metrics_cards)}
            </div>
            
            <div class="info-box status-box-{status_class}" style="margin-top: 20px;">
                <h3>{status_icon} {status_text}</h3>
                <p>{self._get_status_description(estado_global)}</p>
            </div>
        </div>
        """
    
    def _determine_global_status(self) -> str:
        """Determina el estado global del servicio"""
        statuses = []
        
        if self.baseline_data:
            verification = self.baseline_data.get('verificacion', {})
            conclusion = verification.get('conclusion', '')
            if 'exitosa' in conclusion.lower():
                statuses.append('OK')
            else:
                statuses.append('WARNING')
        
        if self.validation_data:
            exec_summary = self.validation_data.get('resumen_ejecutivo', {})
            metricas = exec_summary.get('metricas', {})
            try:
                fallidos = int(metricas.get('Fallidos', '0'))
                revisar = int(metricas.get('Revisar', '0'))
                if fallidos > 0:
                    statuses.append('FAIL')
                elif revisar > 0:
                    statuses.append('WARNING')
                else:
                    statuses.append('OK')
            except:
                statuses.append('UNKNOWN')
        
        if self.predictions_data:
            # Asumimos OK si hay datos
            statuses.append('OK')
        
        # Lógica de prioridad: FAIL > WARNING > OK
        if 'FAIL' in statuses:
            return 'FAIL'
        elif 'WARNING' in statuses:
            return 'WARNING'
        elif 'OK' in statuses:
            return 'OK'
        else:
            return 'UNKNOWN'
    
    def _get_status_description(self, status: str) -> str:
        """Obtiene descripción del estado global"""
        if status == 'OK':
            return "Todos los procesos de validación han sido completados exitosamente. El equipo está correctamente alineado y listo para uso en producción."
        elif status == 'WARNING':
            return "Algunos resultados requieren revisión. Consultar las secciones detalladas para más información."
        elif status == 'FAIL':
            return "La validación ha fallado. El equipo requiere ajustes antes de ser utilizado en producción."
        else:
            return "Estado de validación indeterminado. Revisar informes individuales."
    
    def _generate_baseline_summary(self) -> str:
        """Genera resumen extenso parseado del baseline"""
        info_cliente = self.baseline_data.get('info_cliente', {})
        diagnostico = self.baseline_data.get('diagnostico_wstd', {})
        detalles = self.baseline_data.get('detalles_proceso', {})
        stats = self.baseline_data.get('estadisticas_correccion', {})
        baseline_info = self.baseline_data.get('baseline_generado', {})
        verificacion = self.baseline_data.get('verificacion', {})
        
        # Construir tabla info cliente
        info_rows = []
        for key, value in info_cliente.items():
            info_rows.append(f"<tr><td><strong>{key}</strong></td><td>{value}</td></tr>")
        
        # Construir diagnóstico
        diagnostico_html = ""
        if diagnostico.get('metricas'):
            diag_rows = []
            for key, value in diagnostico['metricas'].items():
                diag_rows.append(f"<tr><td><strong>{key}</strong></td><td>{value}</td></tr>")
            diagnostico_html = f"""
            <h3>Diagnóstico WSTD Inicial</h3>
            <p><strong>Estado:</strong> {diagnostico.get('estado', 'N/A')}</p>
            <table>
                {''.join(diag_rows)}
            </table>
            """
        
        # Construir estadísticas
        stats_rows = []
        for key, value in stats.items():
            stats_rows.append(f"<tr><td><strong>{key}</strong></td><td>{value}</td></tr>")
        
        # Construir verificación
        verif_html = ""
        if verificacion.get('metricas'):
            verif_rows = []
            for key, value in verificacion['metricas'].items():
                verif_rows.append(f"<tr><td><strong>{key}</strong></td><td>{value}</td></tr>")
            verif_html = f"""
            <h3>Verificación Post-Ajuste</h3>
            <table>
                {''.join(verif_rows)}
            </table>
            <p style="margin-top: 15px;"><em>{verificacion.get('conclusion', '')}</em></p>
            """
        
        return f"""
        <h3>Información del Cliente y Equipo</h3>
        <table>
            {''.join(info_rows)}
        </table>
        
        {diagnostico_html}
        
        <h3 style="margin-top: 30px;">Estadísticas de la Corrección</h3>
        <table>
            {''.join(stats_rows)}
        </table>
        
        {verif_html}
        """
    
    def _generate_validation_summary(self) -> str:
        """Genera resumen extenso parseado de validación"""
        service_info = self.validation_data.get('info_servicio', {})
        exec_summary = self.validation_data.get('resumen_ejecutivo', {})
        criterios = self.validation_data.get('criterios_validacion', {})
        global_stats = self.validation_data.get('estadisticas_globales', {})
        detailed = self.validation_data.get('resultados_detallados', [])
        
        # Información del servicio
        service_rows = []
        for key, value in service_info.items():
            service_rows.append(f"<tr><td><strong>{key}</strong></td><td>{value}</td></tr>")
        
        # Métricas del resumen ejecutivo
        metrics = exec_summary.get('metricas', {})
        
        # Criterios de validación
        criterios_html = ""
        if criterios.get('criterios'):
            criterios_rows = []
            for criterio in criterios['criterios']:
                criterios_rows.append(f"""
                    <tr>
                        <td><strong>{criterio['parametro']}</strong></td>
                        <td>{criterio['umbral']}</td>
                        <td>{criterio['descripcion']}</td>
                    </tr>
                """)
            criterios_html = f"""
            <h3 style="margin-top: 30px;">Criterios de Validación</h3>
            <table>
                <tr>
                    <th>Parámetro</th>
                    <th>Umbral</th>
                    <th>Descripción</th>
                </tr>
                {''.join(criterios_rows)}
            </table>
            """
        
        # Resultados detallados
        detail_rows = []
        for result in detailed:
            status_class = result['estado'].lower()
            status_icon = {
                'ok': '✅',
                'warning': '⚠️',
                'fail': '❌'
            }.get(status_class, 'ℹ️')
            
            detail_rows.append(f"""
                <tr>
                    <td>{result['estandar']}</td>
                    <td>{result['correlacion']}</td>
                    <td>{result['max_diff']}</td>
                    <td>{result['rms']}</td>
                    <td>{status_icon} {result['estado']}</td>
                </tr>
            """)
        
        # Estadísticas globales
        stats_rows = []
        for metric_data in global_stats.get('metricas_agregadas', []):
            stats_rows.append(f"""
                <tr>
                    <td><strong>{metric_data['metrica']}</strong></td>
                    <td>{metric_data['minimo']}</td>
                    <td>{metric_data['maximo']}</td>
                    <td>{metric_data['media']}</td>
                    <td>{metric_data['desv_est']}</td>
                </tr>
            """)
        
        return f"""
        <h3>Información del Servicio</h3>
        <table>
            {''.join(service_rows)}
        </table>
        
        <h3 style="margin-top: 30px;">Resumen de Resultados</h3>
        <div class="metrics-grid">
            <div class="metric-card total">
                <div class="metric-value">{metrics.get('Total Estándares', '0')}</div>
                <div class="metric-label">Total</div>
            </div>
            <div class="metric-card ok">
                <div class="metric-value">{metrics.get('Validados', '0')}</div>
                <div class="metric-label">✅ Validados</div>
            </div>
            <div class="metric-card warning">
                <div class="metric-value">{metrics.get('Revisar', '0')}</div>
                <div class="metric-label">⚠️ Revisar</div>
            </div>
            <div class="metric-card fail">
                <div class="metric-value">{metrics.get('Fallidos', '0')}</div>
                <div class="metric-label">❌ Fallidos</div>
            </div>
        </div>
        
        {criterios_html}
        
        <h3 style="margin-top: 30px;">Estadísticas Globales</h3>
        <table>
            <tr>
                <th>Métrica</th>
                <th>Mínimo</th>
                <th>Máximo</th>
                <th>Media</th>
                <th>Desv. Est.</th>
            </tr>
            {''.join(stats_rows)}
        </table>
        
        <h3 style="margin-top: 30px;">Resultados por Estándar</h3>
        <table>
            <tr>
                <th>Estándar</th>
                <th>Correlación</th>
                <th>Max Diferencia (AU)</th>
                <th>RMS</th>
                <th>Estado</th>
            </tr>
            {''.join(detail_rows)}
        </table>
        """
    
    def _generate_predictions_summary(self) -> str:
        """Genera resumen extenso parseado de predicciones"""
        info_general = self.predictions_data.get('info_general', {})
        productos = self.predictions_data.get('productos', [])
        
        # Información de lámparas
        lamparas_html = ""
        if info_general.get('Lámparas'):
            lamparas_list = info_general['Lámparas']
            lamparas_items = ''.join([f"<li>{lamp}</li>" for lamp in lamparas_list])
            lamparas_html = f"""
            <div style="margin-top: 15px;">
                <strong>Lámparas Comparadas:</strong>
                <ul style="margin-top: 10px;">
                    {lamparas_items}
                </ul>
            </div>
            """
        
        # Construir primeros 3 productos como ejemplo
        productos_html = []
        for producto in productos[:3]:
            lamparas_rows = []
            for lampara in producto['lamparas']:
                params_cells = []
                for param in producto['parametros'][:4]:  # Primeros 4 parámetros
                    value = lampara.get(param, 'N/A')
                    params_cells.append(f"<td>{value}</td>")
                
                lamparas_rows.append(f"""
                    <tr>
                        <td class="lamp-name">{lampara.get('Lámpara', 'N/A')}</td>
                        <td>{lampara.get('N', 'N/A')}</td>
                        {''.join(params_cells)}
                    </tr>
                """)
            
            param_headers = ''.join([f"<th>{p.split('|')[0]}</th>" for p in producto['parametros'][:4]])
            
            productos_html.append(f"""
                <h4 style="margin-top: 20px;">{producto['nombre']}</h4>
                <table>
                    <thead>
                        <tr>
                            <th>Lámpara</th>
                            <th>N</th>
                            {param_headers}
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(lamparas_rows)}
                    </tbody>
                </table>
            """)
        
        if len(productos) > 3:
            productos_html.append(f"<p style='margin-top: 15px;'><em>... y {len(productos) - 3} productos más (ver informe completo)</em></p>")
        
        return f"""
        <h3>Información General</h3>
        <table>
            <tr><td><strong>Sensor NIR</strong></td><td>{info_general.get('Sensor NIR', 'N/A')}</td></tr>
            <tr><td><strong>Fecha del Reporte</strong></td><td>{info_general.get('Fecha del Reporte', 'N/A')}</td></tr>
            <tr><td><strong>Productos Analizados</strong></td><td>{info_general.get('Productos Analizados', 'N/A')}</td></tr>
            <tr><td><strong>Lámparas Comparadas</strong></td><td>{info_general.get('Lámparas Comparadas', 'N/A')}</td></tr>
        </table>
        
        {lamparas_html}
        
        <h3 style="margin-top: 30px;">Resultados por Producto (Vista previa)</h3>
        <p style="color: #6c757d; font-size: 0.95em;">
            <em>Mostrando primeros productos. Para ver todos los resultados y gráficos, expandir informe completo.</em>
        </p>
        
        {''.join(productos_html)}
        """
    
    def _generate_index(self) -> str:
        """Genera los items del índice lateral"""
        items = ['<li><a href="#resumen-ejecutivo">📊 Resumen Ejecutivo</a></li>']
        
        if self.baseline_html:
            items.append('<li><a href="#baseline">📐 Baseline Adjustment</a></li>')
        
        if self.validation_html:
            items.append('<li><a href="#validation">✅ Validación Óptica</a></li>')
        
        if self.predictions_html:
            items.append('<li><a href="#predictions">🔬 Predicciones</a></li>')
        
        return '\n'.join(items)
    
    def _generate_collapsible_section(self, section_id: str, title: str, parsed_summary: str, html_content: str) -> str:
        """Genera una sección colapsable con resumen parseado + iframe del HTML completo"""
        # Escapar HTML para srcdoc (reemplazar comillas dobles)
        escaped_html = html_content.replace('"', '&quot;').replace('\n', ' ')
        
        return f"""
        <div class="report-section" id="{section_id}">
            <details>
                <summary class="section-header">
                    <h2>{title}</h2>
                </summary>
                
                <div class="parsed-content">
                    {parsed_summary}
                </div>
                
                <details class="full-report-toggle">
                    <summary class="view-full-report">
                        🔍 Ver Informe Original Completo
                    </summary>
                    <div class="iframe-container">
                        <iframe srcdoc="{escaped_html}" 
                                style="width:100%; height:800px; border:1px solid #ddd; border-radius:5px;">
                        </iframe>
                    </div>
                </details>
            </details>
        </div>
        """
    
    def _generate_footer(self) -> str:
        """Genera el footer del informe"""
        return """
        <div style="text-align: center; margin-top: 50px; padding: 20px; border-top: 2px solid #f8f9fa; color: #6c757d;">
            <p><strong>NIR Maintenance Consolidator v2.0</strong> - Desarrollado para BUCHI</p>
            <p>Informe consolidado generado automáticamente</p>
        </div>
        """
    
    def _get_styles(self) -> str:
        """Retorna los estilos CSS"""
        return """
/* ===== ESTILOS CORPORATIVOS BUCHI ===== */

body { 
    font-family: Helvetica, Arial, sans-serif; 
    margin: 0;
    background-color: #ffffff;
    color: #000000;
    font-size: 14px;
}

/* ===== Sidebar ===== */
.sidebar {
    position: fixed;
    left: 0;
    top: 0;
    width: 250px;
    height: 100%;
    background-color: #093A34;
    padding: 20px;
    overflow-y: auto;
    z-index: 1000;
}

.sidebar h2 {
    color: white;
    font-size: 16px;
    margin-bottom: 20px;
    text-align: center;
}

.sidebar ul {
    list-style: none;
    padding: 0;
}

.sidebar ul li {
    margin-bottom: 10px;
}

.sidebar ul li a {
    color: white;
    text-decoration: none;
    display: block;
    padding: 8px;
    border-radius: 5px;
    transition: background-color 0.3s;
    font-weight: bold;
    font-size: 14px;
}

.sidebar ul li a:hover {
    background-color: #289A93;
}

/* ===== Main Content ===== */
.main-content {
    margin-left: 270px;
    padding: 40px;
}

h1 { 
    color: #000000;
    margin-top: 0px;
    font-weight: bold;
}

h2 { 
    color: #000000;
    font-weight: bold;
    margin-top: 20px;
}

h3 {
    color: #000000;
    margin-top: 15px;
}

h4 {
    color: #000000;
    margin-top: 10px;
}

/* ===== Info Box ===== */
.info-box {
    background-color: #ffffff;
    padding: 25px;
    margin: 25px 0;
    border-radius: 10px;
    border: 1px solid #ddd;
}

/* ===== Collapsible Sections ===== */
.report-section {
    background-color: #ffffff;
    padding: 20px;
    margin: 25px 0;
    border-radius: 10px;
    border: 1px solid #ddd;
}

.report-section > details {
    margin: 0;
}

.report-section > details > summary {
    cursor: pointer;
    user-select: none;
    list-style: none;
    padding: 15px;
    background-color: #f8f9fa;
    border-radius: 8px;
    transition: background-color 0.3s;
}

.report-section > details > summary::-webkit-details-marker {
    display: none;
}

.report-section > details > summary::before {
    content: '▶ ';
    display: inline-block;
    margin-right: 10px;
    transition: transform 0.3s;
}

.report-section > details[open] > summary::before {
    transform: rotate(90deg);
}

.report-section > details > summary:hover {
    background-color: #e9ecef;
}

.section-header h2 {
    display: inline;
    margin: 0;
    font-size: 1.5em;
}

.parsed-content {
    padding: 20px 0;
}

/* ===== Full Report Toggle (nested collapsible) ===== */
.full-report-toggle {
    margin-top: 30px;
    border-top: 2px solid #e9ecef;
    padding-top: 20px;
}

.full-report-toggle > summary {
    cursor: pointer;
    user-select: none;
    list-style: none;
    padding: 12px 20px;
    background: linear-gradient(135deg, #64B445 0%, #289A93 100%);
    color: white;
    border-radius: 8px;
    font-weight: bold;
    font-size: 1.1em;
    transition: opacity 0.3s;
    text-align: center;
}

.full-report-toggle > summary::-webkit-details-marker {
    display: none;
}

.full-report-toggle > summary::before {
    content: '🔍 ';
}

.full-report-toggle[open] > summary::before {
    content: '🔼 ';
}

.full-report-toggle > summary:hover {
    opacity: 0.9;
}

.iframe-container {
    margin-top: 20px;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

/* ===== Tablas ===== */
table { 
    border-collapse: collapse; 
    margin: 20px 0; 
    width: 100%;
    border-radius: 10px;
    overflow: hidden;
}

table, th, td { 
    border: 1px solid #ddd;
}

th { 
    padding: 12px 10px; 
    text-align: left; 
    font-size: 14px;
    background-color: #f8f9fa;
    color: #000000;
    font-weight: bold;
}

td { 
    padding: 10px; 
    text-align: left; 
    font-size: 13px;
    background-color: #ffffff;
    color: #000000;
}

tr:hover {
    background-color: #f5f5f5;
}

.lamp-name {
    font-weight: bold;
    background-color: #f8f9fa;
}

/* ===== Metrics Grid ===== */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin: 20px 0;
}

.metric-card {
    padding: 20px;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.metric-card.ok {
    background-color: #e8f5e9;
    border-left: 4px solid #4caf50;
}

.metric-card.warning {
    background-color: #fff3e0;
    border-left: 4px solid #ff9800;
}

.metric-card.fail {
    background-color: #ffebee;
    border-left: 4px solid #f44336;
}

.metric-card.total {
    background-color: #e3f2fd;
    border-left: 4px solid #2196f3;
}

.metric-card.info {
    background-color: #f8f9fa;
    border-left: 4px solid #64B445;
}

.metric-value {
    font-size: 36px;
    font-weight: bold;
    margin-bottom: 5px;
    color: #000000;
}

.metric-value-small {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 5px;
    color: #000000;
}

.metric-label {
    font-size: 14px;
    color: #666;
    font-weight: bold;
}

.metric-sublabel {
    font-size: 12px;
    color: #999;
    margin-top: 5px;
}

/* ===== Status Boxes ===== */
.status-box-ok {
    background-color: #e8f5e9 !important;
    border-left: 4px solid #4caf50 !important;
}

.status-box-warning {
    background-color: #fff3e0 !important;
    border-left: 4px solid #ff9800 !important;
}

.status-box-fail {
    background-color: #ffebee !important;
    border-left: 4px solid #f44336 !important;
}

.status-box-info {
    background-color: #e3f2fd !important;
    border-left: 4px solid #2196f3 !important;
}

/* ===== Responsive ===== */
@media screen and (max-width: 992px) {
    .sidebar {
        display: none;
    }
    
    .main-content {
        margin-left: 0;
        padding: 20px;
    }
}

@media print {
    .sidebar {
        display: none;
    }
    
    .main-content {
        margin-left: 0;
    }
    
    .full-report-toggle {
        display: none;
    }
}
"""