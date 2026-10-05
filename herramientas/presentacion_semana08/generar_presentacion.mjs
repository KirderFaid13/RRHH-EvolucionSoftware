import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import { pathToFileURL, fileURLToPath } from 'node:url';

// Sin instalación de dependencias. Usa el runtime de presentaciones disponible.
const skillDir = process.env.SKILL_DIR;
const workspaceDir = path.resolve(process.argv[2] ?? '.');
const finalPath = path.resolve(process.argv[3] ?? path.join(workspaceDir, 'docs/semanas/semana08/Semana08_GCS_RRHH.pptx'));
const relativeFinalPath = path.relative(workspaceDir, finalPath);
if (relativeFinalPath.startsWith('..' + path.sep) || path.isAbsolute(relativeFinalPath)) {
  throw new Error('La salida debe permanecer dentro del directorio del proyecto.');
}
const canonicalPath = path.join(workspaceDir, 'docs/semanas/semana08/Semana08_GCS_RRHH.pptx');
const publicDelivery = finalPath === canonicalPath;
const buildDir = path.join(workspaceDir, '.local/c06/presentacion');
const sourceDir = path.dirname(fileURLToPath(import.meta.url));
if (!path.isAbsolute(skillDir ?? '') || !path.isAbsolute(process.env.RUNTIME_PYTHON ?? '')) {
  throw new Error('Defina SKILL_DIR y RUNTIME_PYTHON mediante rutas absolutas.');
}
const { importRuntimeModule } = await import(pathToFileURL(path.join(skillDir, 'container_tools/runtime_helpers.mjs')).href);
const { Presentation, PresentationFile, FileBlob } = await importRuntimeModule('@oai/artifact-tool');
const { finalizePresentation } = await import(pathToFileURL(path.join(skillDir, 'container_tools/artifact_tool_utils.mjs')).href);
const content = JSON.parse(await fs.readFile(path.join(sourceDir, 'contenido_verificado.json'), 'utf8'));
const auditPath = path.join(workspaceDir, 'evidencia/semanas/semana08/auditoria_configuracion.json');
const verificationPath = path.join(workspaceDir, 'evidencia/semanas/semana08/verificacion_configuracion.json');
const audit = JSON.parse(await fs.readFile(auditPath, 'utf8'));
const verification = JSON.parse(await fs.readFile(verificationPath, 'utf8'));
if (content.slideCount !== 8 || content.titles.length !== 8 || content.notes.length !== 8 ||
    content.baselineCommit !== audit.base?.commit || !audit.ok ||
    audit.base?.archivos_versionados !== 531 || audit.resumen?.archivos_verificados !== 531 ||
    audit.resumen?.fallos !== 0 || audit.fallos?.length !== 0 || !verification.ok ||
    verification.pruebas_auditor?.aprobadas !== content.auditScenarios ||
    verification.pruebas_auditor?.total !== content.auditScenarios ||
    verification.pruebas_auditor?.escenarios?.length !== content.auditScenarios ||
    !verification.pruebas_auditor?.escenarios?.every(x => x.ok === true) ||
    verification.v4?.library?.exit_code !== 0 || verification.v4?.library?.source_count !== 22 ||
    verification.v4?.test_compilation?.exit_code !== 0 ||
    verification.v4?.test_compilation?.source_count !== 10 ||
    verification.v4?.tests?.exit_code !== 0 || verification.v4?.tests?.scenarios_passed !== 16 ||
    verification.v4?.tests?.connection_opened !== false) {
  throw new Error('La presentación exige ocho diapositivas y evidencia válida: 531 archivos auditados, cero fallos, 14 escenarios del auditor y 16 escenarios v4 sin SQL.');
}
await fs.mkdir(buildDir, { recursive: true });
await fs.mkdir(path.dirname(finalPath), { recursive: true });
const C = { ink:'#173747', teal:'#007C87', gray:'#526773', white:'#FFFFFF', line:'#C9D6DB', pale:'#EFF5F7' };
const presentation = Presentation.create({ slideSize: { width:1280, height:720 } });
function text(slide, name, value, x, y, w, h, size=28, options={}) {
  const shape = slide.shapes.add({geometry:'textbox',name,position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
  shape.text = value;
  shape.text.style = {typeface:'Arial',fontSize:size,color:options.color??C.ink,bold:options.bold??false,alignment:options.align??'left',verticalAlignment:'top',autoFit:'none',wrap:'square',insets:{left:0,right:0,top:0,bottom:0},lineSpacing:1.06};
  return shape;
}
function slide(n) {
  const s = presentation.slides.add();
  s.background.fill=C.white;
  text(s, `titulo-${n}`, content.titles[n-1], 64, 46, 1150, 72, 43, {bold:true});
  text(s, `pagina-${n}`, String(n), 1190, 663, 30, 30, 18, {color:C.gray,align:'right'});
  s.speakerNotes.textFrame.setText(content.notes[n-1]);
  return s;
}
function pair(s, n, label, value, y, options={}) {
  text(s, `etiqueta-${n}`,label,64,y,options.labelWidth??325,64,options.labelSize??28,{bold:true,color:C.teal});
  text(s, `detalle-${n}`,value,options.detailX??420,y,options.detailWidth??790,options.height??76,options.size??28);
}

{
  const s=slide(1);
  text(s,'semana','Caso práctico de semana 08',64,158,1120,46,28,{color:C.teal,bold:true});
  text(s,'proposito','Control de código, documentos\ny cambios del proyecto',64,248,1120,150,56,{bold:true});
  text(s,'alcance','RRHH original y evolución académica hasta v4',64,467,1120,52,31);
  text(s,'entrega','Preparación C06 sobre la línea base C05',64,553,1120,48,27,{color:C.gray});
}
{
  const s=slide(2);
  pair(s,'procedencia','Procedencia', 'Originales, recuperación parcial y mejoras\nrequieren una identificación distinta.',170);
  pair(s,'sobrescritura','Sobrescritura', 'Editar sin coordinar puede reemplazar\nel trabajo de otra persona.',287);
  pair(s,'evidencia','Evidencia', 'Código y documentación deben indicar\na qué etapa y comprobación pertenecen.',404);
  pair(s,'datos','Datos locales', 'Claves, respaldos y configuraciones reales\nrequieren almacenamiento fuera de Git.',521);
}
{
  const s=slide(3);
  const table=s.tables.add({rows:7,columns:3,left:64,top:145,width:1150,height:448,columnWidths:[350,505,295],values:content.inventoryRows});
  table.styleOptions={headerRow:true,bandedRows:false};
  table.borders.assign({style:'solid',fill:C.line,width:1});
  for(let r=0;r<7;r++) {
    table.rows[r].height=64;
    for(let c=0;c<3;c++) {
      const cell=table.getCell(r,c);
      cell.fill=r===0?C.ink:C.white;
      cell.text.style={typeface:'Arial',fontSize:23,color:r===0?C.white:C.ink,bold:r===0,autoFit:'none'};
    }
  }
  table.cells.block({row:0,column:0,rowCount:7,columnCount:3}).assign({margins:{left:12,right:12,top:4,bottom:4},anchor:'center'});
  text(s,'tabla-aclaracion','El informe amplía las categorías. .local/ permanece fuera de Git.',64,628,1140,32,23,{color:C.gray});
}
{
  const s=slide(4);
  text(s,'estructura-izquierda','.context/ y specs/\nContexto y contratos\n\nsrc/v1/ hasta src/v4/\nFuentes por etapa\n\nlegado/\nReferencia original',64,166,540,414,29);
  text(s,'estructura-derecha','configuracion/\nInventario, cambios y planes\n\ndocs/ y evidencia/\nExplicación y comprobaciones\n\nherramientas/ y referencias/\nScripts y material del curso',654,166,560,414,29);
  text(s,'local','Copia privada en .local/, excluida mediante .gitignore',64,615,1140,38,25,{color:C.teal,bold:true});
}
{
  const s=slide(5);
  pair(s,'versiones','Git y GitHub', 'Historial local y repositorio\nRRHH-EvolucionSoftware.',157);
  pair(s,'base','Línea base C05', 'main, commit 6d82f9f\n531 archivos versionados.',271);
  pair(s,'rama','Preparación C06', 'Rama semana-08-gcs\nSexto commit pendiente.',385);
  text(s,'regla','Una etapa por commit, con qué cambió, por qué\ny qué comprobaciones respaldan el resultado.',64,531,1150,90,31,{bold:true});
}
{
  const s=slide(6);
  pair(s,'registro','1. Registrar', 'CAM-S08-001 describe alcance, motivo\ny archivos que pueden cambiar.',151,{labelWidth:330});
  pair(s,'coordinar','2. Coordinar', 'El autor anuncia las rutas antes de editar\ny trabaja en la rama de la semana.',264);
  pair(s,'comprobar','3. Comprobar', 'Auditoría, pruebas y documentación\nacompañan la propuesta de integración.',377);
  pair(s,'revision','4. Revisar e integrar', 'KirderFaid13 revisa el cambio\ny decide cuándo incorporarlo a main.',490,{labelSize:27});
  text(s,'proceso-estado','Procedimiento propuesto para las siguientes integraciones',64,618,1130,32,23,{color:C.gray});
}
{
  const s=slide(7);
  text(s,'ejecutadas-titulo','Comprobaciones ejecutadas',64,157,1150,44,29,{bold:true,color:C.teal});
  text(s,'ejecutadas-detalle',`16 escenarios v4 con sustitutos, sin SQL.\n${verification.pruebas_auditor.aprobadas} escenarios aislados del auditor de configuración.`,64,217,1150,96,32);
  text(s,'propuestas-titulo','Pruebas iniciales propuestas',64,360,1150,44,29,{bold:true,color:C.teal});
  text(s,'propuestas-detalle','Funcionales de interfaz e integración con SQL.\nRendimiento y seguridad con criterios acordados.\nPendientes de un entorno autorizado.',64,420,1150,135,30);
  text(s,'clasificacion','Caja negra, blanca o gris indica acceso al interior.\nFuncionalidad, rendimiento o seguridad indica el objetivo.',64,600,1150,60,23,{color:C.gray});
}
{
  const s=slide(8);
  text(s,'auditor-comando','python herramientas/auditar_configuracion.py',64,157,1150,47,28,{color:C.teal,bold:true});
  text(s,'auditor-resultado','531 archivos de la base comprobados',64,253,1150,67,42,{bold:true});
  text(s,'auditor-detalle','Contenido protegido conservado.\nCambios autorizados separados de los archivos nuevos.\nCero fallos de configuración en la preparación.',64,359,1150,143,31);
  text(s,'beneficio','Cada etapa mantiene su origen y evidencia\nantes de que el responsable la integre.',64,541,1150,86,30);
}

const candidatePath=path.join(buildDir,'candidate-' + path.basename(finalPath));
await (await PresentationFile.exportPptx(presentation)).save(candidatePath);
const receiptPath=path.join(buildDir,path.basename(finalPath)+'.validation.json');
await finalizePresentation({workspaceDir,candidatePath,finalPath,explicitTotalSlideCount:8,requiredNativeTableOwnerSlides:[3],requiredNativeChartOwnerSlides:[],pythonExecutable:process.env.RUNTIME_PYTHON,integrityValidatorPath:path.join(skillDir,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skillDir,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit','--validate-heading-punctuation','--require-native-table-slide','3'],fontPolicy:{basis:'design',families:['Arial']},verifyArtifactToolImport:true,receiptPath});
const checked=await PresentationFile.importPptx(await FileBlob.load(finalPath));
for(let i=0;i<8;i++) {
  const current=checked.slides.getItem(i);
  const png=await checked.export({slide:current,format:'png',scale:1.5});
  await fs.writeFile(path.join(buildDir,`diapositiva_${i+1}.png`),new Uint8Array(await png.arrayBuffer()));
  const layout=await current.export({format:'layout'});
  await fs.writeFile(path.join(buildDir,`diapositiva_${i+1}.layout.json`),await layout.text());
}
const montage=await checked.export({format:'png',montage:true,scale:0.55});
const previewPath = publicDelivery ? path.join(workspaceDir,'docs/semanas/semana08/vista_previa.png') : path.join(buildDir,path.basename(finalPath)+'.vista_previa.png');
await fs.writeFile(previewPath,new Uint8Array(await montage.arrayBuffer()));
const digest=async file=>crypto.createHash('sha256').update(await fs.readFile(file)).digest('hex');
const evidence={id:'C06-S08',fecha:'2026-10-05',archivo:'docs/semanas/semana08/Semana08_GCS_RRHH.pptx',sha256:await digest(finalPath),diapositivas:8,notas:8,tabla_nativa:[3],texto_editable:true,comprobaciones:{archivos_base:531,escenarios_auditor:verification.pruebas_auditor.aprobadas,escenarios_v4:verification.v4.tests.scenarios_passed,conexion_sql:false},fuentes:{auditoria:{ruta:'evidencia/semanas/semana08/auditoria_configuracion.json',sha256:await digest(auditPath)},verificacion:{ruta:'evidencia/semanas/semana08/verificacion_configuracion.json',sha256:await digest(verificationPath)}},validacion:{estructura_paquete:'PASS',geometria:'PASS',importacion_artifact_tool:'PASS',renderizado_final:'ocho diapositivas importadas del PPTX final',revision_visual:'pendiente de inspección individual',apertura_en_powerpoint:false},limites:['La vista previa y el PPTX local se generan con Artifact Tool, independientemente de Canva.','No se atribuye equivalencia funcional completa ni conexión con SQL.','El sexto commit y la integración siguen pendientes.']};
await fs.mkdir(path.join(workspaceDir,'evidencia/semanas/semana08'),{recursive:true});
evidence.archivo = relativeFinalPath.split(path.sep).join('/');
const evidencePath = publicDelivery ? path.join(workspaceDir,'evidencia/semanas/semana08/presentacion.json') : path.join(buildDir,path.basename(finalPath)+'.presentacion.json');
await fs.writeFile(evidencePath,JSON.stringify(evidence,null,2)+'\n');
console.log(JSON.stringify({finalPath,receiptPath,slides:8,notes:8,nativeTable:[3]},null,2));
