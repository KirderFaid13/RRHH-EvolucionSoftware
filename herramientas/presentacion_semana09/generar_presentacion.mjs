import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath, pathToFileURL } from 'node:url';

// Ejecutar con el runtime local de presentaciones. No instala paquetes.
const workspaceDir = path.resolve(process.argv[2] ?? '.');
const sourceDir = path.dirname(fileURLToPath(import.meta.url));
const canonicalFinal = path.join(workspaceDir, 'docs/semanas/semana09/Semana09_Gestion_Cambio_RRHH.pptx');
const finalPath = path.resolve(process.argv[3] ?? canonicalFinal);
const contentPath = path.resolve(process.argv[4] ?? path.join(sourceDir, 'contenido_verificado.json'));
const skillDir = process.env.SKILL_DIR;
const runtimePython = process.env.RUNTIME_PYTHON;
for (const [name, value] of Object.entries({ SKILL_DIR: skillDir, RUNTIME_PYTHON: runtimePython })) {
  if (!path.isAbsolute(value ?? '')) throw new Error(`${name} debe ser una ruta absoluta.`);
}
function inWorkspace(target) {
  const relative = path.relative(workspaceDir, target);
  if (relative === '..' || relative.startsWith('..' + path.sep) || path.isAbsolute(relative)) {
    throw new Error('El contenido y las salidas deben permanecer dentro del proyecto.');
  }
}
inWorkspace(finalPath);
inWorkspace(contentPath);
if (await fs.stat(finalPath).catch(() => null)) throw new Error('La salida ya existe. Use otro nombre para una revisión.');
const privateRoot = path.join(workspaceDir, '.local/c07/presentacion');
const stem = path.basename(finalPath, path.extname(finalPath));
const candidatePath = path.join(privateRoot, 'borradores', `${stem}.candidate.pptx`);
const receiptPath = path.join(privateRoot, 'recibos', `${stem}.validation.json`);
const renderDir = path.join(privateRoot, `render-${stem}`);
for (const dir of [path.dirname(candidatePath), path.dirname(receiptPath), path.dirname(finalPath), renderDir]) {
  await fs.mkdir(dir, { recursive: true });
}
const { importRuntimeModule } = await import(pathToFileURL(path.join(skillDir, 'container_tools/runtime_helpers.mjs')).href);
const { Presentation, PresentationFile, FileBlob } = await importRuntimeModule('@oai/artifact-tool');
const { finalizePresentation } = await import(pathToFileURL(path.join(skillDir, 'container_tools/artifact_tool_utils.mjs')).href);
const content = JSON.parse(await fs.readFile(contentPath, 'utf8'));
const slides = content.slides;
if (!Array.isArray(slides) || !slides.length) throw new Error('El contenido debe definir slides[].');
if (finalPath === canonicalFinal && slides.length !== 26) throw new Error('La entrega final debe contener 26 diapositivas.');
for (const [index, slide] of slides.entries()) {
  if (!slide.titulo || !Array.isArray(slide.visible) || !slide.nota || !Array.isArray(slide.fuentes)) {
    throw new Error(`Diapositiva ${index + 1}: faltan título, texto visible, nota o fuentes.`);
  }
}

const C = { ivory: '#F6F1E8', navy: '#11233E', blue: '#2456A6', copper: '#A75C32', soft: '#D4DDEB', line: '#C9C4BA' };
const presentation = Presentation.create({ slideSize: { width: 1280, height: 720 } });
const tableOwnerSlides = [];
function text(s, name, value, x, y, w, h, size = 32, options = {}) {
  const shape = s.shapes.add({ geometry: 'textbox', name, position: { left: x, top: y, width: w, height: h }, fill: 'none', line: { fill: 'none', width: 0 } });
  shape.text = String(value);
  shape.text.style = {
    typeface: options.font ?? 'Arial', fontSize: size, color: options.color ?? C.navy,
    bold: options.bold ?? false, alignment: options.align ?? 'left', verticalAlignment: 'top',
    autoFit: 'none', wrap: 'square', lineSpacing: 1.08,
    insets: { left: 0, right: 0, top: 0, bottom: 0 },
  };
  return shape;
}
function countLines(value, width, size, font = 'Arial') {
  // Estimación conservadora solo para repartir espacio. La revisión visual manda.
  const average = size * (font === 'Consolas' ? 0.61 : 0.50);
  return String(value).split('\n').reduce((sum, line) => sum + Math.max(1, Math.ceil(line.length * average / width)), 0);
}
function bodyLines(s, values, x, y, w, h, color, options = {}) {
  const size = options.size ?? 32;
  const lineHeight = size * 1.20;
  const gap = options.gap ?? 19;
  const heights = values.map(v => countLines(v, w, size) * lineHeight + 5);
  const availableGap = values.length > 1 ? Math.min(gap, Math.max(8, (h - heights.reduce((a, b) => a + b, 0)) / (values.length - 1))) : 0;
  let top = y;
  values.forEach((value, i) => {
    text(s, `contenido-${i + 1}`, value, x, top, w, heights[i], size, { color, bold: options.firstBold && i === 0 });
    top += heights[i] + availableGap;
  });
  return top;
}
function normalized(v) { return String(v).toLowerCase().normalize('NFD').replace(/\p{Diacritic}/gu, '').replace(/[^a-z0-9 ]/g, ' ').replace(/\s+/g, ' ').trim(); }
function exampleIsRedundant(item) {
  if (!item.ejemplo) return true;
  const body = normalized(item.visible.join(' '));
  const example = normalized(item.ejemplo);
  const words = example.split(' ').filter(w => w.length > 4);
  const common = words.filter(w => body.includes(w)).length;
  return body.includes(example) || (words.length > 0 && common / words.length >= 0.60);
}
async function cover(s, item) {
  s.background.fill = C.ivory;
  const b = await fs.readFile(path.join(sourceDir, 'assets/portada_conceptual.png'));
  s.images.add({ blob: b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength), contentType: 'image/png', alt: 'Ilustración conceptual generada con IA: hojas de software transparentes unidas por una bisagra de cobre.', fit: 'cover', position: { left: 0, top: 0, width: 1280, height: 720 } });
  text(s, 'titulo-portada', item.titulo, 64, 64, 505, 190, 56, { bold: true });
  const values = item.visible;
  text(s, 'proposito-portada', values[0] ?? '', 64, 276, 494, 108, 32, { color: C.blue });
  // El segundo nombre y el docente necesitan dos líneas a 30 px.
  const authorPositions = [
    { y: 404, h: 45 },
    { y: 454, h: 85 },
    { y: 544, h: 85 },
    { y: 639, h: 43 },
  ];
  for (let i = 1; i < values.length; i++) {
    const frame = authorPositions[i - 1] ?? { y: 640 + (i - 4) * 42, h: 42 };
    text(s, `autoria-${i}`, values[i], 64, frame.y, 510, frame.h, 30);
  }
}
function table(s, number, rows, isDark, item) {
  if (!Array.isArray(rows) || rows.length < 2 || !Array.isArray(rows[0])) throw new Error(`Tabla inválida en diapositiva ${number}.`);
  const columns = rows[0].length;
  if (!rows.every(r => r.length === columns)) throw new Error('Tabla con filas de distinta longitud.');
  tableOwnerSlides.push(number);
  const top = item.tableTop ?? 198;
  const height = item.tableHeight ?? 390;
  let widths = item.columnWidths;
  if (!widths) {
    if (columns === 2) widths = [782, 370];
    else if (columns === 3) widths = [230, 510, 412];
    else if (columns === 4) widths = [230, 220, 400, 302];
    else widths = Array.from({ length: columns }, () => 1152 / columns);
  }
  const t = s.tables.add({ rows: rows.length, columns, left: 64, top, width: 1152, height, columnWidths: widths, values: rows.map(r => r.map(String)) });
  t.styleOptions = { headerRow: true, bandedRows: false };
  t.borders.assign({ style: 'solid', fill: isDark ? '#526079' : C.line, width: 0.8 });
  const rowHeight = height / rows.length;
  for (let r = 0; r < rows.length; r++) {
    t.rows[r].height = rowHeight;
    for (let c = 0; c < columns; c++) {
      const cell = t.getCell(r, c);
      cell.fill = r === 0 ? (isDark ? C.ivory : C.navy) : (isDark ? C.navy : C.ivory);
      cell.text.style = { typeface: 'Arial', fontSize: item.tableFontSize ?? 30, color: r === 0 ? (isDark ? C.navy : C.ivory) : (isDark ? C.ivory : C.navy), bold: r === 0, autoFit: 'none' };
    }
  }
  t.cells.block({ row: 0, column: 0, rowCount: rows.length, columnCount: columns }).assign({ margins: { left: 14, right: 14, top: 8, bottom: 8 }, anchor: 'center' });
  const tail = item.visible.filter(v => !rows.flat().includes(v));
  if (tail.length) bodyLines(s, tail, 64, top + height + 24, 1152, 68, isDark ? C.soft : C.blue, { size: 30, gap: 8 });
}
function codeSlide(s, number, item, isDark) {
  const fg = isDark ? C.ivory : C.navy;
  const accent = isDark ? C.ivory : C.blue;
  const before = Array.isArray(item.before) ? item.before.join('\n') : item.before;
  const after = Array.isArray(item.after) ? item.after.join('\n') : item.after;
  if (!before) throw new Error('Una diapositiva de código exige before.');
  if (!after) {
    text(s, 'codigo-comandos-editable', before, 64, 235, 1152, 152, item.codeFontSize ?? 30, { color: fg, font: 'Consolas' });
    bodyLines(s, item.visible, 64, 447, 1152, 190, fg, { size: 32, gap: 24 });
    return;
  }
  text(s, 'antes-etiqueta', item.beforeLabel ?? 'v4 · Antes', 64, 195, 540, 45, 32, { color: accent, bold: true });
  text(s, 'despues-etiqueta', item.afterLabel ?? 'v5 · Después', 664, 195, 552, 45, 32, { color: accent, bold: true });
  const codeSize = item.codeFontSize ?? 25;
  text(s, 'codigo-antes-editable', before, 64, 270, 540, 252, codeSize, { color: fg, font: 'Consolas' });
  text(s, 'codigo-despues-editable', after, 664, 270, 552, 252, codeSize, { color: fg, font: 'Consolas' });
  bodyLines(s, item.visible, 64, 555, 1152, 92, fg, { size: 30, gap: 8 });
}

for (const [index, item] of slides.entries()) {
  const number = index + 1;
  const isDark = number % 2 === 0;
  const fg = isDark ? C.ivory : C.navy;
  const accent = isDark ? C.ivory : C.blue;
  const s = presentation.slides.add();
  s.background.fill = isDark ? C.navy : C.ivory;
  s.speakerNotes.textFrame.setText(item.nota + '\n\nFuentes y procedencia:\n' + item.fuentes.join('\n'));
  if (number === 1) {
    await cover(s, item);
  } else {
    text(s, `titulo-${number}`, item.titulo, 64, 60, 1152, 123, 54, { color: fg, bold: true });
    if (item.kind === 'code') {
      codeSlide(s, number, item, isDark);
    } else if (item.kind === 'matrix' || item.tableRows) {
      table(s, number, item.tableRows, isDark, item);
    } else if (item.kind === 'evidence' && item.metrics) {
      const metrics = Array.isArray(item.metrics) ? item.metrics : Object.entries(item.metrics);
      const rows = [['Comprobación', 'Resultado'], ...metrics.map(m => Array.isArray(m) ? m : [m.label ?? m.etiqueta ?? m.nombre ?? m.comprobacion, m.value ?? m.valor ?? m.resultado])];
      table(s, number, rows, isDark, { ...item, tableTop: 200, tableHeight: rows.length * 75, tableFontSize: 32 });
      const nativeTable = s.tables.items[s.tables.items.length - 1];
      const resultColor = number === 21 ? '#A03C2D' : (isDark ? '#9CD1B7' : '#1F6650');
      for (let r = 1; r < rows.length; r++) {
        nativeTable.getCell(r, 1).text.style = { typeface: 'Arial', fontSize: 34, color: resultColor, bold: true, autoFit: 'none' };
      }
    } else if (number === 7 || item.kind === 'process' || item.kind === 'flow') {
      const rows = item.visible;
      const stages = rows.filter(v => /^\d\s/.test(v));
      const rest = rows.filter(v => !/^\d\s/.test(v));
      if (stages.length === 8) {
        bodyLines(s, stages.slice(0, 4), 64, 218, 535, 320, fg, { size: 38, gap: 32 });
        bodyLines(s, stages.slice(4), 664, 218, 552, 320, fg, { size: 38, gap: 32 });
        if (rest.length) bodyLines(s, rest, 64, 575, 1152, 74, accent, { size: 32 });
      } else bodyLines(s, rows, 64, 210, 1152, 425, fg, { size: 33 });
    } else if ([3, 4, 5, 6].includes(number)) {
      const values = item.visible;
      const headline = values[0];
      text(s, 'proposito-tipo', headline, 64, 214, 1100, 93, 43, { color: fg, bold: true });
      const rest = values.slice(1);
      bodyLines(s, rest, 64, 343, 1152, 248, fg, { size: 34, gap: 22 });
    } else {
      const showExample = item.showExample === true && !exampleIsRedundant(item) && ![15, 16, 26].includes(number);
      const top = 215;
      const values = item.visible;
      const bottom = showExample ? 515 : 638;
      const count = values.length;
      const bodySize = count <= 3 ? 38 : count <= 5 ? 34 : 32;
      bodyLines(s, values, 64, top, 1152, bottom - top, fg, { size: bodySize, gap: count <= 4 ? 30 : 21, firstBold: count <= 3 });
      if (showExample) text(s, 'ejemplo-concreto', item.ejemplo, 64, 559, 1152, 96, 30, { color: isDark ? C.soft : C.copper });
    }
  }
  text(s, `pie-${number}`, String(number).padStart(2, '0'), 1152, 672, 64, 25, 18, { color: isDark && number !== 1 ? C.soft : C.navy, align: 'right' });
}

await (await PresentationFile.exportPptx(presentation)).save(candidatePath);
await finalizePresentation({
  workspaceDir, candidatePath, finalPath,
  explicitTotalSlideCount: slides.length,
  requiredNativeTableOwnerSlides: tableOwnerSlides,
  requiredNativeChartOwnerSlides: [],
  pythonExecutable: runtimePython,
  integrityValidatorPath: path.join(skillDir, 'container_tools/inspect_presentation_package_integrity.py'),
  layoutValidatorPath: path.join(skillDir, 'container_tools/inspect_presentation_layout_geometry.py'),
  layoutArgs: ['--expected-slide-size-emu', '12192000,6858000', '--validate-heading-fit', '--validate-heading-punctuation', ...tableOwnerSlides.flatMap(n => ['--require-native-table-slide', String(n)])],
  fontPolicy: { basis: 'design', families: ['Arial', 'Consolas'] },
  verifyArtifactToolImport: true,
  receiptPath,
});
const checked = await PresentationFile.importPptx(await FileBlob.load(finalPath));
for (let i = 0; i < slides.length; i++) {
  const current = checked.slides.getItem(i);
  const png = await checked.export({ slide: current, format: 'png', scale: 1 });
  await fs.writeFile(path.join(renderDir, `diapositiva_${String(i + 1).padStart(2, '0')}.png`), new Uint8Array(await png.arrayBuffer()));
  const layout = await current.export({ format: 'layout' });
  await fs.writeFile(path.join(renderDir, `diapositiva_${String(i + 1).padStart(2, '0')}.layout.json`), await layout.text());
}
const montage = await checked.export({ format: 'png', montage: true, scale: 0.30 });
await fs.writeFile(path.join(renderDir, 'vista_general.png'), new Uint8Array(await montage.arrayBuffer()));
const sha256 = async p => crypto.createHash('sha256').update(await fs.readFile(p)).digest('hex');
const receipt = {
  archivo: path.relative(workspaceDir, finalPath).split(path.sep).join('/'),
  sha256: await sha256(finalPath), contenido_sha256: await sha256(contentPath),
  diapositivas: slides.length, notas: slides.length, tablas_nativas: tableOwnerSlides,
  texto_editable: true, codigo_editable: slides.filter(x => x.kind === 'code').length,
  fuentes: ['Arial', 'Consolas'], ancho: 1280, alto: 720,
  render_importacion_final: true, revision_visual: 'pendiente de inspección individual',
  apertura_powerpoint: false, registro_validacion: path.relative(workspaceDir, receiptPath).split(path.sep).join('/'),
};
await fs.writeFile(path.join(privateRoot, `${stem}.resumen.json`), JSON.stringify(receipt, null, 2) + '\n');
console.log(JSON.stringify({ finalPath, receiptPath, renderDir, slides: slides.length, nativeTables: tableOwnerSlides, sha256: receipt.sha256 }, null, 2));
