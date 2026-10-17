import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';

// Revisión editorial independiente. La autoría modifica solo quince páginas.
// El bloque práctico se conserva como partes Open XML originales, sin roundtrip.
const workspaceDir = path.resolve(process.argv[2] ?? '.');
const sourceDir = path.dirname(fileURLToPath(import.meta.url));
const contentPath = path.resolve(process.argv[3] ?? path.join(sourceDir, 'contenido_teoria_revisada.json'));
const finalPath = path.resolve(process.argv[4] ?? path.join(workspaceDir, 'docs/semanas/semana09/Semana09_Gestion_Cambio_RRHH_Teoria_Revisada.pptx'));
const sourcePath = path.join(workspaceDir, 'docs/semanas/semana09/Semana09_Gestion_Cambio_RRHH.pptx');
const skillDir = process.env.SKILL_DIR;
const runtimePython = process.env.RUNTIME_PYTHON;
if (!path.isAbsolute(skillDir ?? '') || !path.isAbsolute(runtimePython ?? '')) throw new Error('Declare SKILL_DIR y RUNTIME_PYTHON absolutos.');
for (const target of [contentPath, finalPath]) {
  const relative = path.relative(workspaceDir, target);
  if (relative.startsWith('..') || path.isAbsolute(relative)) throw new Error('Las salidas deben permanecer dentro del workspace.');
}
if (await fs.stat(finalPath).catch(() => null)) throw new Error('El archivo final ya existe; elija otro nombre para revisar.');
const buildDir = path.join(workspaceDir, '.local/c07/teoria_revision');
const stem = path.basename(finalPath, '.pptx');
const runDir = path.join(buildDir, stem + '-' + Date.now());
const theoryPath = path.join(runDir, 'teoria15.pptx');
const candidatePath = path.join(runDir, 'combinada26.candidate.pptx');
const receiptPath = path.join(runDir, 'validacion.json');
const preservationPath = path.join(runDir, 'preservacion.json');
const renderDir = path.join(runDir, 'renders');
await fs.mkdir(renderDir, { recursive: true });
await fs.mkdir(path.dirname(finalPath), { recursive: true });
const { importRuntimeModule } = await import(pathToFileURL(path.join(skillDir, 'container_tools/runtime_helpers.mjs')).href);
const { Presentation, PresentationFile, FileBlob } = await importRuntimeModule('@oai/artifact-tool');
const { finalizePresentation } = await import(pathToFileURL(path.join(skillDir, 'container_tools/artifact_tool_utils.mjs')).href);
const originalContent = JSON.parse(await fs.readFile(path.join(sourceDir, 'contenido_verificado.json'), 'utf8'));
const content = JSON.parse(await fs.readFile(contentPath, 'utf8'));
if (content.slides?.length !== 26) throw new Error('Se requieren exactamente 26 diapositivas.');
if (JSON.stringify(content.slides.slice(15)) !== JSON.stringify(originalContent.slides.slice(15))) {
  throw new Error('Los datos de las páginas prácticas deben ser idénticos al contenido histórico.');
}
for (const [index, item] of content.slides.slice(0, 15).entries()) {
  if (!item.titulo || !item.nota || !item.ejemplo || !Array.isArray(item.visible) || !Array.isArray(item.fuentes)) {
    throw new Error(`Diapositiva ${index + 1}: faltan concepto, ejemplo, contenido o notas.`);
  }
  const text = [item.titulo, ...item.visible, item.ejemplo, item.nota].join('\n');
  if (/\b(RRHH|CMI|Dispose|using|C07)\b|CAM-S09|Issue\s*#\s*(10|11|12)\b/i.test(text)) {
    throw new Error(`Referencia al proyecto en teoría ${index + 1}.`);
  }
}
const C = { ivory: '#F6F1E8', navy: '#11233E', blue: '#2456A6', copper: '#A75C32', soft: '#D4DDEB', line: '#C9C4BA' };
const presentation = Presentation.create({ slideSize: { width: 1280, height: 720 } });
const nativeTheoryTables = [];
function text(slide, name, value, x, y, w, h, size = 32, options = {}) {
  const shape = slide.shapes.add({ geometry: 'textbox', name,
    position: { left: x, top: y, width: w, height: h }, fill: 'none', line: { fill: 'none', width: 0 } });
  shape.text = String(value);
  shape.text.style = { typeface: 'Arial', fontSize: size, color: options.color ?? C.navy,
    bold: options.bold ?? false, alignment: options.align ?? 'left', verticalAlignment: 'top',
    autoFit: 'none', wrap: 'square', lineSpacing: 1.08,
    insets: { left: 0, right: 0, top: 0, bottom: 0 } };
  return shape;
}
function example(slide, item, fg, y = 576, size = 30) {
  text(slide, 'ejemplo-visible', item.ejemplo, 64, y, 1152, 88, size, { color: fg });
}
function splitField(value) {
  const at = value.indexOf(':');
  return at < 0 ? ['Regresión', value] : [value.slice(0, at), value.slice(at + 1).trim()];
}
function nativeTable(slide, number, rows, dark, options = {}) {
  const top = options.top ?? 280;
  const height = options.height ?? 280;
  const widths = options.widths ?? [285, 867];
  const table = slide.tables.add({ rows: rows.length, columns: rows[0].length,
    left: 64, top, width: 1152, height, columnWidths: widths, values: rows });
  table.styleOptions = { headerRow: true, bandedRows: false };
  table.borders.assign({ style: 'solid', fill: dark ? '#526079' : C.line, width: 0.8 });
  for (let r = 0; r < rows.length; r++) {
    table.rows[r].height = height / rows.length;
    for (let c = 0; c < rows[0].length; c++) {
      const cell = table.getCell(r, c);
      cell.fill = r === 0 ? (dark ? C.ivory : C.navy) : (dark ? C.navy : C.ivory);
      cell.text.style = { typeface: 'Arial', fontSize: options.size ?? 30,
        color: r === 0 ? (dark ? C.navy : C.ivory) : (dark ? C.ivory : C.navy), bold: r === 0, autoFit: 'none' };
    }
  }
  table.cells.block({ row: 0, column: 0, rowCount: rows.length, columnCount: rows[0].length })
    .assign({ margins: { left: 14, right: 14, top: 8, bottom: 8 }, anchor: 'center' });
  nativeTheoryTables.push(number);
}
async function cover(slide, item) {
  const bytes = await fs.readFile(path.join(sourceDir, 'assets/portada_conceptual.png'));
  slide.images.add({ blob: bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength),
    contentType: 'image/png', alt: 'Ilustración conceptual de capas de software unidas por una bisagra.', fit: 'cover',
    position: { left: 0, top: 0, width: 1280, height: 720 } });
  text(slide, 'titulo-portada', item.titulo, 64, 64, 505, 190, 56, { bold: true });
  text(slide, 'proposito-portada', item.visible[0], 64, 278, 494, 108, 32, { color: C.blue });
  for (const [index, row] of item.visible.slice(1).entries()) {
    const y = [404, 454, 544, 639][index];
    text(slide, `autoria-${index}`, row, 64, y, 510, index === 0 || index === 3 ? 44 : 85, 30);
  }
}
for (const [index, item] of content.slides.slice(0, 15).entries()) {
  const number = index + 1;
  const dark = number % 2 === 0;
  const fg = dark ? C.ivory : C.navy;
  const accent = dark ? C.soft : C.copper;
  const slide = presentation.slides.add();
  slide.background.fill = dark ? C.navy : C.ivory;
  slide.speakerNotes.textFrame.setText(item.nota + '\n\nFuentes y procedencia:\n' + item.fuentes.join('\n'));
  if (number === 1) await cover(slide, item);
  else {
    if (number === 2) {
      const bytes = await fs.readFile(path.join(sourceDir, 'assets/transferencia_entrada_conceptual.png'));
      slide.images.add({ blob: bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength),
        contentType: 'image/png', alt: 'Ejemplo conceptual generado: transferencia de una entrada entre dos teléfonos.',
        fit: 'cover', position: { left: 0, top: 0, width: 1280, height: 720 } });
    }
    text(slide, 'titulo', item.titulo, 64, number === 2 ? 55 : 60,
      number === 2 ? 510 : 1152, number === 2 ? 130 : 123,
      number === 2 ? 48 : 54, { color: fg, bold: true });
    if (number === 2) {
      text(slide, 'definicion', item.visible[0], 64, 205, 465, 200, 36, { color: fg, bold: true });
      text(slide, 'trazabilidad', item.visible[1], 64, 426, 465, 116, 31, { color: fg });
      text(slide, 'ejemplo-visible', item.ejemplo, 64, 562, 465, 102, 29, { color: accent });
    } else if ([3, 4, 5, 6].includes(number)) {
      text(slide, 'definicion-del-tipo', item.visible[0], 64, 210, 472, 250, 46, { color: fg, bold: true });
      text(slide, 'caso-hipotetico', item.visible[1], 630, 214, 586, 210, 36, { color: accent });
      text(slide, 'respuesta-al-caso', item.visible[2], 630, 462, 586, 180, 34, { color: fg });
    } else if (number === 7) {
      const stages = item.stages ?? item.visible.slice(0, 8).map(v => v.replace(/^\d\s+/, ''));
      for (let n = 0; n < 8; n++) {
        const x = 64 + (n % 4) * 298;
        const y = n < 4 ? 214 : 401;
        text(slide, `paso-numero-${n}`, String(n + 1).padStart(2, '0'), x, y, 240, 55, 42, { color: C.blue, bold: true });
        text(slide, `paso-nombre-${n}`, stages[n], x, y + 67, 258, 105, 31, { color: fg });
      }
      example(slide, item, C.copper, 603, 29);
    } else if ([8, 9, 10, 12].includes(number)) {
      text(slide, 'concepto-tabla', item.visible[0], 64, 190, 1152, 84, 36, { color: fg, bold: true });
      const labels = { 8: ['Solicitud', 'Ejemplo definido'], 9: ['Componente', 'Qué se debe evaluar'],
        10: ['Participante', 'Responsabilidad'], 12: ['Escenario', 'Resultado esperado'] };
      const values = item.visible.slice(1).filter(v => !(number === 10 && v.startsWith('Caso:'))).map(splitField);
      nativeTable(slide, number, [labels[number], ...values], dark,
        { top: 285, height: number === 9 ? 285 : 260, widths: [300, 852], size: 30 });
      example(slide, item, accent, number === 9 ? 596 : 580, 29);
    } else if (number === 11) {
      text(slide, 'concepto-plan', item.visible[0], 64, 190, 1152, 86, 36, { color: fg, bold: true });
      for (const [n, value] of item.visible.slice(1).entries()) {
        const [label, description] = splitField(value);
        text(slide, `orden-${n}`, label, 64 + n * 398, 305, 355, 62, 37, { color: C.blue, bold: true });
        text(slide, `actividad-${n}`, description, 64 + n * 398, 388, 355, 150, 32, { color: fg });
      }
      example(slide, item, C.copper, 585, 30);
    } else if (number === 13) {
      text(slide, 'concepto-publicacion', item.visible[0], 64, 190, 1152, 74, 38, { color: fg, bold: true });
      text(slide, 'activacion', 'Activación gradual', 64, 307, 518, 65, 38, { color: C.blue, bold: true });
      text(slide, 'activacion-descripcion', item.visible[1], 64, 397, 518, 130, 33, { color: fg });
      text(slide, 'contingencia', 'Contingencia', 664, 307, 552, 65, 38, { color: C.blue, bold: true });
      text(slide, 'contingencia-descripcion', item.visible[2], 664, 397, 552, 130, 33, { color: fg });
      text(slide, 'limite-reversion', item.visible[3], 64, 563, 1152, 55, 33, { color: C.copper, bold: true });
      example(slide, item, C.navy, 626, 25);
    } else if (number === 14) {
      text(slide, 'concepto-trazabilidad', item.visible[0], 64, 190, 1152, 88, 36, { color: fg, bold: true });
      for (const [n, value] of item.visible.slice(1).entries()) {
        const [label, description] = splitField(value);
        text(slide, `artefacto-${n}`, label, 64 + n * 298, 314, 258, 115, 34, { color: C.soft, bold: true });
        text(slide, `funcion-${n}`, description, 64 + n * 298, 448, 258, 115, 30, { color: fg });
      }
      example(slide, item, accent, 600, 28);
    } else if (number === 15) {
      nativeTable(slide, number, [['Momento', 'Respuesta del ejemplo'], ...item.visible.map(splitField)], dark,
        { top: 209, height: 365, widths: [280, 872], size: 31 });
      example(slide, item, C.copper, 607, 29);
    }
  }
  text(slide, 'numero-pagina', String(number).padStart(2, '0'), 1152, 672, 64, 25, 18,
    { color: dark && number !== 1 ? C.soft : C.navy, align: 'right' });
}
await (await PresentationFile.exportPptx(presentation)).save(theoryPath);
const graft = String.raw`
import hashlib,json,posixpath,re,sys
from zipfile import ZipFile,ZIP_DEFLATED
from xml.etree import ElementTree as ET
source,theory,output,report=sys.argv[1:]
NS='{http://schemas.openxmlformats.org/package/2006/relationships}'
def sha(data): return hashlib.sha256(data).hexdigest()
with ZipFile(source) as original, ZipFile(theory) as authored:
    data={n:original.read(n) for n in original.namelist()}
    replaced=[]; media=[]
    for number in range(1,16):
        slide=f'ppt/slides/slide{number}.xml'
        notes=f'ppt/notesSlides/notesSlide{number}.xml'
        for part in (slide,notes):
            data[part]=authored.read(part); replaced.append(part)
        for part,owner in ((f'ppt/slides/_rels/slide{number}.xml.rels',slide),
                           (f'ppt/notesSlides/_rels/notesSlide{number}.xml.rels',notes)):
            rels=ET.fromstring(authored.read(part))
            for rel in rels:
                kind=rel.attrib['Type'].rsplit('/',1)[-1]
                target=rel.attrib['Target']
                if rel.attrib.get('TargetMode')=='External': continue
                absolute=target.lstrip('/') if target.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(owner),target))
                if kind=='image':
                    renamed='ppt/media/theory_review_'+posixpath.basename(absolute)
                    payload=authored.read(absolute)
                    if renamed in data and data[renamed]!=payload: raise ValueError('Colisión de medios')
                    data[renamed]=payload; rel.attrib['Target']='/'+renamed
                    if renamed not in media: media.append(renamed)
                elif kind=='slideLayout':
                    if absolute!='ppt/slideLayouts/slideLayout6.xml': raise ValueError('Layout generado no previsto')
                    if absolute not in data: raise ValueError('Layout original ausente')
                elif kind=='notesSlide':
                    if absolute!=notes: raise ValueError('Nota cruzada')
                elif kind=='slide':
                    if absolute!=slide: raise ValueError('Relación de nota incorrecta')
                elif kind=='notesMaster':
                    if absolute!='ppt/notesMasters/notesMaster1.xml': raise ValueError('Notes master no previsto')
                else: raise ValueError('Relación nueva no prevista: '+kind)
            data[part]=ET.tostring(rels,encoding='utf-8',xml_declaration=True); replaced.append(part)
    practical=[f'ppt/{folder}/{prefix}{n}.xml' for n in range(16,27) for folder,prefix in [('slides','slide'),('notesSlides','notesSlide')]]
    practical += [f'ppt/{folder}/_rels/{prefix}{n}.xml.rels' for n in range(16,27) for folder,prefix in [('slides','slide'),('notesSlides','notesSlide')]]
    if any(data[n]!=original.read(n) for n in practical): raise ValueError('Bloque práctico alterado')
    unchanged=[n for n in original.namelist() if n not in replaced]
    if any(data[n]!=original.read(n) for n in unchanged): raise ValueError('Parte compartida alterada')
    with ZipFile(output,'x',ZIP_DEFLATED) as final:
        for name,payload in data.items(): final.writestr(name,payload)
    with open(report,'w',encoding='utf-8',newline='\n') as out:
        json.dump({'original_sha256':sha(open(source,'rb').read()),'practical_parts_identical':len(practical),
                   'original_parts_unchanged':len(unchanged),'theory_parts_replaced':len(replaced),
                   'new_media':media,'practical_parts':[{'part':n,'sha256':sha(data[n])} for n in practical]},out,ensure_ascii=False,indent=2)
`;
const assembled = spawnSync(runtimePython, ['-c', graft, sourcePath, theoryPath, candidatePath, preservationPath], { encoding: 'utf8' });
if (assembled.status !== 0) throw new Error('Ensamblado rechazado: ' + assembled.stderr);
const sha256 = async name => crypto.createHash('sha256').update(await fs.readFile(name)).digest('hex');
const requiredTables = [...nativeTheoryTables, 17, 20, 21, 22];
await finalizePresentation({ workspaceDir, candidatePath, finalPath, explicitTotalSlideCount: 26,
  requiredNativeTableOwnerSlides: requiredTables, requiredNativeChartOwnerSlides: [], pythonExecutable: runtimePython,
  integrityValidatorPath: path.join(skillDir, 'container_tools/inspect_presentation_package_integrity.py'),
  layoutValidatorPath: path.join(skillDir, 'container_tools/inspect_presentation_layout_geometry.py'),
  layoutArgs: ['--expected-slide-size-emu', '12192000,6858000', '--validate-heading-fit', '--validate-heading-punctuation',
    ...requiredTables.flatMap(n => ['--require-native-table-slide', String(n)])],
  fontPolicy: { basis: 'reference', families: ['Arial', 'Consolas'], referencePath: sourcePath, referenceSha256: await sha256(sourcePath) },
  verifyArtifactToolImport: true, receiptPath });
if (await sha256(candidatePath) !== await sha256(finalPath)) {
  throw new Error('El finalizador modificó los bytes del candidato ensamblado; revise preservación antes de entregar.');
}
const finalDeck = await PresentationFile.importPptx(await FileBlob.load(finalPath));
const originalDeck = await PresentationFile.importPptx(await FileBlob.load(sourcePath));
const identicalPracticalRenders = [];
for (let n = 0; n < 26; n++) {
  const slide = finalDeck.slides.getItem(n);
  const png = Buffer.from(await (await finalDeck.export({ slide, format: 'png', scale: 1 })).arrayBuffer());
  await fs.writeFile(path.join(renderDir, `diapositiva_${String(n + 1).padStart(2, '0')}.png`), png);
  const layout = await slide.export({ format: 'layout' });
  await fs.writeFile(path.join(renderDir, `diapositiva_${String(n + 1).padStart(2, '0')}.layout.json`), await layout.text());
  if (n >= 15) {
    const before = Buffer.from(await (await originalDeck.export({ slide: originalDeck.slides.getItem(n), format: 'png', scale: 1 })).arrayBuffer());
    if (!png.equals(before)) throw new Error(`El render práctico ${n + 1} difiere del original.`);
    identicalPracticalRenders.push(n + 1);
  }
}
const montage = await finalDeck.export({ format: 'png', montage: true, scale: 0.30 });
await fs.writeFile(path.join(renderDir, 'vista_general.png'), new Uint8Array(await montage.arrayBuffer()));
const result = { finalPath, sha256: await sha256(finalPath), contentSha256: await sha256(contentPath),
  sourceSha256: await sha256(sourcePath), slides: 26, notes: 26, theorySlides: 15,
  requiredNativeTableOwnerSlides: requiredTables, identicalPracticalRenders,
  preservationPath, receiptPath, renderDir, powerpointOpened: false, visualReview: 'pendiente de revisión individual' };
await fs.writeFile(path.join(runDir, 'resumen.json'), JSON.stringify(result, null, 2) + '\n');
console.log(JSON.stringify(result, null, 2));
