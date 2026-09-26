import fs from 'node:fs/promises';
import { FileBlob, SpreadsheetFile } from '@oai/artifact-tool';
const root = 'C:/Users/KABUM/Documents/BERT- Fine';
const wb = await SpreadsheetFile.importXlsx(await FileBlob.load(`${root}/test1.xlsx`));
console.log((await wb.inspect({kind:'workbook', include:'id,sheets'})).ndjson);
console.log((await wb.inspect({kind:'table', range:'test1!A1:B12', include:'values,formulas', maxChars:5000})).ndjson);
const preview = await wb.render({sheetName:'test1', range:'A1:B18', scale:1, format:'png'});
await fs.writeFile(`${root}/runs/etapa7/etapa7_20260926_105326_ca987906/original_preview.png`, Buffer.from(await preview.arrayBuffer()));
