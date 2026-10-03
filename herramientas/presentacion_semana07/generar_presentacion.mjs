import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL, fileURLToPath } from 'node:url';

// Requiere el runtime local de Codex, sin instalar ni modificar dependencias.
// RUNTIME_NODE_MODULES, RUNTIME_PYTHON y SKILL_DIR son rutas absolutas.
const skillDir = process.env.SKILL_DIR;
const workspaceDir = path.resolve(process.argv[2] ?? '.');
const evidencePath = path.resolve(process.argv[3] ?? path.join(workspaceDir, 'evidencia/semanas/semana07/compilacion_y_pruebas.json'));
const buildDir = path.join(workspaceDir, '.local/c05/presentacion');
const finalPath = path.resolve(process.argv[4] ?? path.join(workspaceDir, 'docs/semanas/semana07/Semana07_IoC_RRHH.pptx'));
const receiptPath = path.join(buildDir, path.basename(finalPath) + '.validation.json');
if (!path.isAbsolute(skillDir ?? '') || !path.isAbsolute(process.env.RUNTIME_PYTHON ?? '')) {
  throw new Error('Defina SKILL_DIR y RUNTIME_PYTHON con rutas absolutas del runtime.');
}
const { importRuntimeModule } = await import(pathToFileURL(path.join(skillDir, 'container_tools/runtime_helpers.mjs')).href);
const { Presentation, PresentationFile, FileBlob } = await importRuntimeModule('@oai/artifact-tool');
const { finalizePresentation } = await import(pathToFileURL(path.join(skillDir, 'container_tools/artifact_tool_utils.mjs')).href);
const evidence = JSON.parse(await fs.readFile(evidencePath, 'utf8'));
// Este archivo de contenido se genera solo después de comprobar la evidencia.
const sourceDir = path.dirname(fileURLToPath(import.meta.url));
const content = JSON.parse(await fs.readFile(path.join(sourceDir, 'contenido_verificado.json'), 'utf8'));
if (content.evidenceStatus !== 'PASS' || content.slideCount !== 6 || !content.verifiedEvidence) {
  throw new Error('La presentación exige evidencia PASS revisada y seis diapositivas.');
}
if (evidence.library?.exit_code !== 0 || evidence.test_compilation?.exit_code !== 0 ||
    evidence.tests?.exit_code !== 0 || evidence.tests?.scenarios_passed !== 16 ||
    evidence.tests?.original_contract_scenarios !== 11 || evidence.tests?.connection_opened !== false ||
    evidence.tests?.generator_generar_executed_with_substitute !== true) {
  throw new Error('La evidencia exige compilación correcta y los 16 escenarios aprobados sin abrir SQL.');
}
await fs.mkdir(buildDir, { recursive: true });
await fs.mkdir(path.dirname(finalPath), { recursive: true });
const W = 1280, H = 720;
const C = { ink:'#123548', teal:'#087F8C', gray:'#526B78', pale:'#ECF4F6', code:'#173F50', white:'#FFFFFF', muted:'#B8CDD4' };
const presentation = Presentation.create({ slideSize:{ width:W, height:H } });
function box(slide, name, text, x,y,w,h,size=28,opt={}) {
  const shape = slide.shapes.add({ geometry:opt.geometry??'textbox', name, position:{left:x,top:y,width:w,height:h}, fill:opt.fill??'none', line:{fill:opt.border??'none',width:opt.border?2:0} });
  shape.text = text;
  shape.text.style = { typeface:opt.font??'Arial', fontSize:size, color:opt.color??C.ink, bold:opt.bold??false, alignment:opt.align??'left', verticalAlignment:opt.valign??'top', autoFit:'none', wrap:opt.wrap??'square', insets:{top:0,bottom:0,left:0,right:0}, lineSpacing:1.05 };
  return shape;
}
function slide(title, number, notes) {
  const s = presentation.slides.add(); s.background.fill=C.white;
  box(s,`titulo-${number}`,title,64,46,1140,70,43,{bold:true});
  box(s,`pagina-${number}`,String(number),1190,664,30,30,18,{color:C.gray,align:'right'});
  s.speakerNotes.textFrame.setText(notes);
  return s;
}
function code(slide, name, lines, x,y,w,h,size=25,highlight=[]) {
  // El código es texto editable, no una imagen de pantalla.
  const surface = slide.shapes.add({geometry:'rect',name:`${name}-fondo`,position:{left:x,top:y,width:w,height:h},fill:C.pale,line:{fill:'none',width:0}});
  const lh=size*1.38;
  for(let i=0;i<lines.length;i++)box(slide,`${name}-${i+1}`,lines[i],x+24,y+24+i*lh,w-48,lh,size,{font:'Consolas',color:highlight.includes(i)?C.teal:C.code,bold:highlight.includes(i),wrap:'none'});
  return surface;
}

// 1. Caso y objetivo
{
 const s=slide('Inversión de control en reportes RRHH',1,content.notes[0]);
 box(s,'caso-etiqueta','Caso práctico de semana 07',64,162,1080,44,27,{color:C.teal,bold:true});
 box(s,'caso-objeto','GeneradorReportes',64,240,1110,90,58,{bold:true});
 box(s,'caso-objetivo','Permitir que el código que usa el generador\nelija cómo ejecutar un reporte.',64,356,1110,120,38);
 box(s,'caso-problema','Dependencia fija en v3: EjecutorReportesSql',64,548,1100,50,26,{color:C.gray});
}
// 2. Código anterior real
{
 const s=slide('Antes: el generador elige el ejecutor SQL',2,content.notes[1]);
 box(s,'antes-origen','v3 / caso_reportes / GeneradorReportes.cs',64,130,1100,32,21,{color:C.gray});
 code(s,'antes',[
   'private readonly EjecutorReportesSql _sql;',
   '',
   'public GeneradorReportes(SqlConnection conexion,',
   '                        SqlDataAdapter adaptador)',
   '{',
   '    _conexion = conexion;',
   '    _sql = new EjecutorReportesSql(conexion, adaptador);',
   '}'
 ],64,188,1150,352,28,[0,6]);
 box(s,'antes-limitacion','Generar queda ligado a SQL. Una prueba completa necesita\nsustituir la ejecución, pero v3 no permite hacerlo.',64,572,1150,90,29);
}
// 3. Después: contrato y constructor
{
 const s=slide('Después: el constructor recibe la dependencia',3,content.notes[2]);
 box(s,'despues-interface-label','Contrato de ejecución',64,134,1000,38,23,{color:C.teal,bold:true});
 code(s,'interfaz',[
   'public interface IEjecutorReportes',
   '{',
   '    DataSet Ejecutar(ComandoReporte reporte);',
   '}'
 ],64,182,1150,162,24,[0,2]);
 box(s,'despues-generador-label','GeneradorReportes en v4',64,370,1000,38,23,{color:C.teal,bold:true});
 code(s,'inyeccion',[
   'private readonly IEjecutorReportes _sql;',
   'public GeneradorReportes(SqlConnection conexion, IEjecutorReportes sql)',
   '{',
   '    _conexion = conexion;',
   '    _sql = sql;',
   '}'
 ],64,414,1150,224,22,[0,4]);
}
// 4. Composición manual
{
 const s=slide('La composición crea los objetos fuera del generador',4,content.notes[3]);
 box(s,'composicion-subtitulo','ComposicionReportes.CrearSql(conexion, adaptador)',64,137,1150,42,26,{font:'Consolas',color:C.teal});
 const factory=box(s,'composicion-factory','Composición\nmanual',64,236,300,116,31,{geometry:'rect',border:C.teal,align:'center',valign:'middle'});
 const executor=box(s,'composicion-sql','EjecutorReportesSql\ncon conexión y adaptador',478,206,724,108,30,{geometry:'rect',border:C.teal,align:'center',valign:'middle'});
 const generator=box(s,'composicion-generador','GeneradorReportes\nrecibe conexión y ejecutor',478,389,724,108,30,{geometry:'rect',border:C.teal,align:'center',valign:'middle'});
 s.shapes.connect(factory,executor,{kind:'elbow',fromSide:'right',toSide:'left',line:{fill:C.teal,width:2},tail:{type:'triangle',width:'med',length:'med'}});
 s.shapes.connect(factory,generator,{kind:'elbow',fromSide:'bottom',toSide:'left',line:{fill:C.teal,width:2},tail:{type:'triangle',width:'med',length:'med'}});
 s.shapes.connect(executor,generator,{kind:'straight',fromSide:'bottom',toSide:'top',line:{fill:C.teal,width:2},tail:{type:'triangle',width:'med',length:'med'}});
 box(s,'composicion-paso1','crea',375,236,84,40,21,{color:C.gray,align:'center'});
 box(s,'composicion-paso2','crea',375,403,84,36,21,{color:C.gray,align:'center'});
 box(s,'composicion-entrega','se entrega',865,334,150,36,21,{color:C.gray});
 box(s,'composicion-sin-container','La fachada usa CrearSql(...).Generar(definicion).\nEl caso utiliza inyección por constructor y composición manual.',64,550,1130,94,28);
}
// 5. Demostración verificada
{
 const s=slide('Generar completo funciona con un sustituto',5,content.notes[4]);
 box(s,'pruebas-estado','PASS',64,156,360,82,60,{color:C.teal,bold:true});
 box(s,'pruebas-conteo',content.resultSummary,64,258,1100,56,35,{bold:true});
 box(s,'pruebas-flujo','GeneradorReportes recibe un IEjecutorReportes de prueba.\nEl sustituto registra el ComandoReporte y devuelve un DataSet conocido.',64,352,1140,92,29);
 box(s,'pruebas-detalle',content.resultDetails.join('\n'),64,488,1140,148,27);
}
// 6. Aporte y límites del caso
{
 const s=slide('Aporte y límites de esta mejora',6,content.notes[5]);
 box(s,'aportes-label','Aporte de IoC',64,154,1120,42,29,{color:C.teal,bold:true});
 box(s,'aportes','El generador recibe el ejecutor.\nUn sustituto permite probar Generar sin ejecutar SQL.',64,218,1120,104,32);
 box(s,'limites-label','Límites comprobables',64,382,1120,42,29,{color:C.teal,bold:true});
 box(s,'limites','Preparar sigue utilizando SqlConnection.\nLa ejecución SQL conserva su código ADO.NET.\nLa integración con la base real continúa pendiente.',64,452,1120,156,31);
}

const candidatePath=path.join(buildDir,'candidate-' + path.basename(finalPath));
await (await PresentationFile.exportPptx(presentation)).save(candidatePath);
const finalized=await finalizePresentation({
 workspaceDir,candidatePath,finalPath,
 explicitTotalSlideCount:6,
 requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[],
 pythonExecutable:process.env.RUNTIME_PYTHON,
 integrityValidatorPath:path.join(skillDir,'container_tools/inspect_presentation_package_integrity.py'),
 layoutValidatorPath:path.join(skillDir,'container_tools/inspect_presentation_layout_geometry.py'),
 layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit','--validate-heading-punctuation'],
 fontPolicy:{basis:'design',families:['Arial','Consolas']},
 verifyArtifactToolImport:true,
 receiptPath
});
// Renderizamos el archivo final importado, no solo el modelo antes de exportar.
const checked = await PresentationFile.importPptx(await FileBlob.load(finalPath));
for(let i=0;i<6;i++) {
 const slide=checked.slides.getItem(i);
 const png=await checked.export({slide,format:'png',scale:1.5});
 await fs.writeFile(path.join(buildDir,`diapositiva_${i+1}.png`),new Uint8Array(await png.arrayBuffer()));
 const layout=await slide.export({format:'layout'});
 await fs.writeFile(path.join(buildDir,`diapositiva_${i+1}.layout.json`),await layout.text());
}
const montage=await checked.export({format:'png',montage:true,scale:0.55});
await fs.writeFile(path.join(workspaceDir,'docs/semanas/semana07/vista_previa.png'),new Uint8Array(await montage.arrayBuffer()));
console.log(JSON.stringify({finalPath,receipt:receiptPath,slides:6,result:finalized},null,2));
