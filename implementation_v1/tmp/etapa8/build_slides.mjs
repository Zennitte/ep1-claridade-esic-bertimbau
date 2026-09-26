import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { Presentation, PresentationFile } from '@oai/artifact-tool';

const workspaceDir = 'C:\\Users\\KABUM\\Documents\\BERT- Fine';
const buildDir = path.join(workspaceDir, 'tmp', 'etapa8');
const finalPath = path.join(workspaceDir, 'outputs', 'etapa8', 'apresentacao_ep1.pptx');
const skillDir = 'C:\\Users\\KABUM\\.codex\\plugins\\cache\\openai-primary-runtime\\presentations\\26.909.12148\\skills\\presentations';
const python = 'C:\\Users\\KABUM\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe';
const { finalizePresentation } = await import(pathToFileURL(path.join(skillDir,'container_tools','artifact_tool_utils.mjs')).href);
await fs.mkdir(path.dirname(finalPath), {recursive:true});
const deck = Presentation.create({slideSize:{width:1280,height:720}});
const navy='#142A3B', blue='#146C94', gray='#526674', white='#FFFFFF';
function box(slide, value, x,y,w,h,size=24,bold=false,color=navy){
  const shape=slide.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
  shape.text=value;
  shape.text.style={typeface:'Arial',fontSize:size,bold,color,autoFit:'none'};
  return shape;
}
function base(title, number){
  const s=deck.slides.add(); s.background.fill=white;
  box(s,title,64,45,1150,82,37,true,navy);
  box(s,`${number} / 8`,1150,654,65,25,15,false,gray);
  return s;
}
function line(s, text, y, size=24, color=navy){box(s,text,78,y,1090,50,size,false,color);}
function notes(s,text){s.speakerNotes.textFrame.setText(text);}

let s=deck.slides.add(); s.background.fill=white;
box(s,'Clareza das respostas e-SIC',72,150,1120,90,51,true,navy);
box(s,'Classificação em três classes com BERTimbau Base',76,255,1070,55,28,false,blue);
box(s,'EP1  •  ACH2118',76,460,500,42,23,false,gray);
box(s,'[NOMES E NÚMEROS USP DOS INTEGRANTES]',76,514,1070,38,20,false,gray);
notes(s,'Apresentar a tarefa e os integrantes. Substituir os placeholders antes da apresentação. Fonte: enunciado do EP1 e relatório do projeto.');

s=base('Tarefa e conjunto de dados',2);
box(s,'20.092',80,155,410,100,66,true,blue);
box(s,'respostas rotuladas para treino',85,258,600,48,25,false,navy);
line(s,'c1: 6.347    c234: 6.853    c5: 6.892',365,29);
line(s,'900 respostas sem rótulo no arquivo de teste',449,25);
line(s,'A métrica de teste não pode ser calculada sem rótulos.',523,23,gray);
notes(s,'Fonte: reports/etapa1_audit.md e reports/etapa7_inferencia.md. Não apresentar distribuição de predições como acurácia.');

s=base('Divisão e prevenção de vazamento',3);
box(s,'17.068',80,160,400,85,60,true,blue);
box(s,'desenvolvimento',84,246,470,50,25,false,navy);
box(s,'3.024',720,160,400,85,60,true,blue);
box(s,'holdout externo',724,246,450,50,25,false,navy);
line(s,'Três folds internos com StratifiedGroupKFold',365,27);
line(s,'Textos equivalentes permanecem no mesmo grupo',445,25);
line(s,'Holdout consultado uma vez, após congelar a configuração',520,24,gray);
notes(s,'Fonte: reports/etapa1_audit.md e reports/etapa5f_holdout_audit.md. A normalização NFC, casefold e colapso de espaços foi usada somente para a chave de grupo.');

s=base('Busca e escolha do modelo',4);
line(s,'BERTimbau Base com cabeça nova para c1, c234 e c5',165,26);
line(s,'8 combinações: posição do texto, 256 ou 512 tokens,',265,25);
line(s,'taxa de 2 × 10⁻⁵ ou 3 × 10⁻⁵',311,25);
box(s,'Escolhido',80,410,330,55,25,true,blue);
box(s,'início + 512 tokens + 2 × 10⁻⁵',80,467,1060,65,34,true,navy);
line(s,'Regra prévia: maior acurácia média nos três folds',565,22,gray);
notes(s,'Fontes: reports/etapa4_search.md e reports/etapa5e_final_spec.md. Não alegar superioridade estável com base na triagem inicial.');

s=base('Confirmação nos três folds',5);
box(s,'45,007%',80,160,500,100,66,true,blue);
box(s,'acurácia média do BERTimbau',85,268,700,50,25,false,navy);
line(s,'TF-IDF + regressão logística: 44,705%',379,28);
line(s,'Diferença média: +0,302 ponto percentual',447,26);
line(s,'Variação entre folds maior que essa diferença',524,24,gray);
notes(s,'Fonte: reports/etapa5e_final_spec.md. A seleção por acurácia foi pré-fixada; o fold 3 ficou abaixo do baseline.');

s=base('Holdout na mesma divisão',6);
box(s,'45,966%',80,153,470,85,58,true,blue);
box(s,'BERTimbau',85,243,350,42,25,false,navy);
box(s,'45,437%',710,153,470,85,58,true,blue);
box(s,'TF-IDF + regressão logística',715,243,480,42,25,false,navy);
line(s,'16 acertos adicionais para o BERT em 3.024 casos',365,25);
line(s,'Macro F1: BERT 44,523%; TF-IDF 45,056%',432,25);
line(s,'McNemar exato: p = 0,590',501,25,gray);
notes(s,'Fontes: reports/etapa5f_holdout_audit.md e reports/etapa5f_tfidf_holdout_comparison.md. A vantagem descritiva em acurácia é pequena; o TF-IDF obteve macro F1 maior.');

s=base('Treino final e inferência',7);
box(s,'20.092',80,150,430,85,60,true,blue);
box(s,'exemplos usados no ajuste final',85,241,710,48,25,false,navy);
line(s,'4.523 atualizações do otimizador, sem ajuste no holdout',348,25);
line(s,'Modelo salvo e aplicado a 900 respostas de teste',422,25);
line(s,'900 rótulos preenchidos em test1_predito.xlsx',496,25);
line(s,'Acurácia de teste: indisponível sem gabarito',566,23,gray);
notes(s,'Fontes: reports/etapa6_final.md e reports/etapa7_inferencia.md. O checkpoint final inclui as linhas antes usadas no holdout; não atribuir a ele a métrica da auditoria.');

s=base('Conclusões e reprodução',8);
line(s,'BERTimbau foi o escolhido pela regra de acurácia prévia.',154,25);
line(s,'A diferença para TF-IDF no holdout é pequena.',230,25);
line(s,'O recall de c234 foi 24,131%: principal limitação.',306,25);
box(s,'Código e configuração',80,408,680,47,26,true,blue);
box(s,'github.com/Zennitte/ep1-claridade-esic-bertimbau',80,461,1080,51,24,false,navy);
line(s,'Relatório no Google Docs; apresentação em Google Slides',561,22,gray);
notes(s,'Fontes: relatórios das etapas 5f, 6 e 7. Para reproduzir, consultar o README do repositório, obter os dados pelo canal autorizado e usar GPU ROCm compatível.');

const candidate=path.join(buildDir,'candidate_ep1.pptx');
await (await PresentationFile.exportPptx(deck)).save(candidate);
for(let i=0;i<deck.slides.length;i++){
  const image=await deck.export({slide:deck.slides.getByIndex(i),format:'png',scale:1});
  await fs.writeFile(path.join(buildDir,`slide-${i+1}.png`),new Uint8Array(await image.arrayBuffer()));
}
const result=await finalizePresentation({
  workspaceDir,candidatePath:candidate,finalPath,
  explicitTotalSlideCount:8,
  requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[],
  pythonExecutable:python,
  integrityValidatorPath:path.join(skillDir,'container_tools','inspect_presentation_package_integrity.py'),
  layoutValidatorPath:path.join(skillDir,'container_tools','inspect_presentation_layout_geometry.py'),
  layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit'],
  fontPolicy:{basis:'design',families:['Arial']},
  verifyArtifactToolImport:true,
  receiptPath:path.join(buildDir,'validation.json'),
});
console.log(JSON.stringify({finalPath,result}));
