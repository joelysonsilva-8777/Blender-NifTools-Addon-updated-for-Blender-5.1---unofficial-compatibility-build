# Blender NifTools Addon para Blender 5.1

Versão experimental e não oficial do **Blender NifTools Addon**, atualizada para instalar, ativar e funcionar melhor no **Blender 5.1** com **Python 3.13**.

Esta build foi criada como um pacote de compatibilidade para quem ainda precisa importar e exportar arquivos **NetImmerse/Gamebryo** (`.nif`, `.kf`, `.egm`) em versões novas do Blender.

[![Blender](https://img.shields.io/badge/Blender-5.1-orange)](#compatibilidade)
[![Python](https://img.shields.io/badge/Python-3.13-blue)](#compatibilidade)
[![Status](https://img.shields.io/badge/status-experimental-yellow)](#aviso-importante)
[![License](https://img.shields.io/badge/license-NifTools%20original-lightgrey)](#créditos-e-licença)

> Esta não é uma versão oficial do projeto NifTools. Use com backup dos seus arquivos e confira o resultado antes de usar em produção.

## Sumário

- [O que esta build faz](#o-que-esta-build-faz)
- [Compatibilidade](#compatibilidade)
- [Instalação](#instalação)
- [Como usar o import/export normal](#como-usar-o-importexport-normal)
- [Tutorial: Niftools Aurakingdom Helper](#tutorial-niftools-aurakingdom-helper)
- [Exportando com conversão DDS para PNG](#exportando-com-conversão-dds-para-png)
- [Principais correções desta atualização](#principais-correções-desta-atualização)
- [Soluções de problemas](#soluções-de-problemas)
- [Limites conhecidos](#limites-conhecidos)
- [Créditos e licença](#créditos-e-licença)

## O que esta build faz

Esta versão mantém a base do Blender NifTools Addon e adiciona correções de compatibilidade para o Blender 5.1, incluindo:

- instalação e ativação do addon no Blender 5.1;
- compatibilidade com mudanças do Python 3.13;
- importação de modelos `.nif` em Blender 5.1;
- importação de animações `.kf` em Blender 5.1;
- busca melhorada de texturas em pastas externas;
- painel auxiliar para jogos com estrutura parecida com Aura Kingdom;
- exportação `.nif` com opção de converter texturas `.dds` carregadas para `.png`.

## Compatibilidade

| Item | Status |
| --- | --- |
| Blender 5.1 / 5.1.1 | Testado nesta build |
| Python 3.13 | Corrigido para ativação e uso básico |
| Blender 3.6 | Mantido quando possível, mas esta build foi focada no Blender 5.1 |
| Import `.nif` | Funcionando nos testes realizados |
| Import `.kf` | Funcionando com a nova API de Actions do Blender 5.1 |
| Export `.nif` | Mantido a partir do addon original, com helper opcional para PNG |

## Instalação

### Opção 1: instalar pelo arquivo ZIP

1. Baixe o ZIP desta build pelo GitHub.
2. Abra o Blender.
3. Vá em `Edit > Preferences > Add-ons`.
4. Clique em `Install...`.
5. Selecione o ZIP.
6. Ative o addon chamado **NetImmerse/Gamebryo format support**.

### Opção 2: instalar manualmente

1. Copie a pasta do addon para a pasta de addons do Blender:

```text
Blender/5.1/scripts/addons/io_scene_niftools
```

No Windows, normalmente fica em:

```text
C:\Users\SEU_USUARIO\AppData\Roaming\Blender Foundation\Blender\5.1\scripts\addons\io_scene_niftools
```

2. Abra o Blender.
3. Vá em `Edit > Preferences > Add-ons`.
4. Procure por `NifTools`, `NIF` ou `NetImmerse`.
5. Ative **NetImmerse/Gamebryo format support**.

## Como usar o import/export normal

Depois de ativar o addon, o Blender deve mostrar as opções tradicionais:

### Importar NIF

1. Vá em `File > Import`.
2. Escolha `NetImmerse/Gamebryo (.nif)`.
3. Selecione o arquivo `.nif`.
4. Ajuste as opções do importador se precisar.
5. Clique em `Import`.

### Importar KF

1. Importe primeiro o modelo `.nif` com a armature.
2. Selecione a armature no Blender.
3. Vá em `File > Import`.
4. Escolha `NetImmerse/Gamebryo (.kf)`.
5. Selecione o arquivo `.kf`.
6. A animação será aplicada na armature selecionada quando os nomes dos bones forem compatíveis.

### Exportar NIF

1. Selecione os objetos que deseja exportar.
2. Vá em `File > Export`.
3. Escolha `NetImmerse/Gamebryo (.nif)`.
4. Configure as opções do exportador.
5. Salve o arquivo.

## Tutorial: Niftools Aurakingdom Helper

Esta build inclui um painel novo no sidebar do Blender:

```text
3D View > Sidebar > Niftools Aurakingdom Helper
```

Para abrir o sidebar, pressione `N` dentro da viewport 3D.

O helper foi feito para jogos que organizam arquivos assim:

```text
game_folder/
  animation/
    M001.kf
    M002.kf

  model/
    M001.nif
    M002.nif

  texture/
    M001.dds
    M001_N.dds
```

### Campos do painel

| Campo | Função |
| --- | --- |
| `Models` | Pasta onde estão os arquivos `.nif` |
| `Refresh Models` | Atualiza a lista de modelos da pasta selecionada |
| `Model` | Campo pesquisável para escolher o `.nif` |
| `Textures` | Pasta onde estão as texturas, geralmente `.dds` |
| `Animations` | Pasta onde estão as animações `.kf` |
| `Use Textures` | Usa a pasta `Textures` durante a importação |
| `Import KF` | Procura uma animação `.kf` com o mesmo nome do `.nif` |
| `Import` | Importa o modelo selecionado |
| `Export` | Pasta de destino do export |
| `Name` | Nome do arquivo exportado, sem extensão |
| `DDS to PNG` | Converte texturas `.dds` carregadas para `.png` ao exportar |
| `Export` | Exporta o `.nif` e, se ativado, salva PNGs das texturas |

### Passo a passo para importar modelo, textura e animação

1. Abra a viewport 3D.
2. Pressione `N` para abrir o sidebar.
3. Entre na aba **Niftools Aurakingdom Helper**.
4. Em `Models`, escolha a pasta `model`.
5. Clique em `Refresh Models`.
6. No campo `Model`, digite parte do nome do arquivo ou escolha na lista pesquisável.
7. Em `Textures`, escolha a pasta `texture`.
8. Em `Animations`, escolha a pasta `animation`.
9. Deixe `Use Textures` ligado se quiser carregar texturas externas.
10. Deixe `Import KF` ligado se quiser que o helper procure uma animação com o mesmo nome.
11. Clique em `Import`.

Exemplo:

```text
model/M001.nif
animation/M001.kf
texture/*.dds
```

Ao importar `M001.nif`, o helper tenta:

- carregar o modelo `M001.nif`;
- procurar texturas na pasta `texture`;
- procurar automaticamente `M001.kf` na pasta `animation`;
- mostrar no painel se a animação ou alguma textura não foi encontrada.

Se a animação não existir, o modelo ainda será importado normalmente.

### Por que existe o botão Refresh Models?

Pastas de jogos podem ter centenas ou milhares de modelos. Um dropdown tradicional do Blender fica lento porque ele tenta reconstruir a lista muitas vezes enquanto a interface redesenha.

Por isso, esta build usa um cache:

1. Você escolhe a pasta `Models`.
2. Clica em `Refresh Models`.
3. O addon lê os `.nif` uma vez.
4. O campo `Model` fica pesquisável e rápido.

Se você trocar a pasta de modelos ou adicionar novos `.nif`, clique em `Refresh Models` novamente.

## Exportando com conversão DDS para PNG

O helper também tem um fluxo rápido de exportação:

1. Escolha a pasta de destino em `Export`.
2. Digite o nome do arquivo em `Name`.
3. Ative `DDS to PNG` se quiser converter texturas `.dds` carregadas.
4. Clique em `Export`.

O addon exporta:

```text
NomeEscolhido.nif
TexturaCarregada.png
OutraTexturaCarregada.png
```

Importante: a conversão para PNG usa as imagens `.dds` que estão carregadas no Blender no momento. Ela não varre a pasta inteira de texturas.

## Principais correções desta atualização

### Ativação no Blender 5.1 / Python 3.13

- Corrigida dependência antiga de `distutils.cmd`, removida no Python 3.13.
- Adicionado fallback interno para manter os módulos empacotados funcionando.

Arquivos relacionados:

```text
dependencies/pyffi/utils/__init__.py
dependencies/nifgen/utils/__init__.py
```

### Registro e desregistro do addon

- Corrigidos callbacks de menu para evitar referências a classes RNA removidas.
- Desregistro ficou mais tolerante a falhas parciais de ativação.
- Logger agora evita crash quando o Blender remove a instância do operador.

Arquivos relacionados:

```text
operators/__init__.py
utils/logging.py
```

### Importação de modelos no Blender 5.1

- Corrigido acesso a `Mesh.use_auto_smooth`, que não existe mais no Blender 5.1.
- Corrigido acesso a `Material.shadow_method`, removido ou alterado nas versões novas.
- Corrigido uso de face maps em versões onde a API não está mais disponível.

Arquivos relacionados:

```text
modules/nif_import/geometry/vertex/__init__.py
modules/nif_import/property/material/__init__.py
modules/nif_import/geometry/vertex/groups.py
```

### Importação de animações KF

- Corrigido uso de `Action.fcurves`, que mudou no Blender 5.1.
- Adicionado suporte para acessar/criar F-Curves pela nova estrutura de actions.
- Mantida compatibilidade com o comportamento antigo quando possível.

Arquivos relacionados:

```text
modules/nif_import/animation/__init__.py
modules/nif_import/animation/transform.py
```

### Busca de texturas

- A pasta de texturas selecionada agora aceita melhor caminhos como:

```text
textures/arquivo.dds
texture/arquivo.dds
subpasta/arquivo.dds
arquivo.dds
```

- Também tenta extensões alternativas como `.dds`, `.png`, `.tga`, `.bmp` e `.jpg`.

Arquivo relacionado:

```text
modules/nif_import/property/texture/loader.py
```

### Niftools Aurakingdom Helper

- Adicionado painel no sidebar da viewport.
- Adicionadas configurações para pastas de modelos, texturas e animações.
- Adicionado import automático de `.kf` correspondente ao `.nif`.
- Adicionado seletor pesquisável de modelos com cache.
- Adicionado export helper com conversão opcional de `.dds` para `.png`.

Arquivos relacionados:

```text
properties/aurakingdom.py
operators/aurakingdom.py
ui/aurakingdom.py
```

## Soluções de problemas

### O addon não aparece na lista

Confira se a pasta está com este nome:

```text
io_scene_niftools
```

E se dentro dela existe o arquivo:

```text
__init__.py
```

Depois reinicie o Blender e procure por `NifTools` ou `NetImmerse`.

### O painel mostra a pasta Models, mas não lista os modelos

Depois de escolher a pasta `Models`, clique em:

```text
Refresh Models
```

O campo `Model` usa cache para não travar em pastas grandes.

### O modelo importou, mas a animação não

Confira:

- se `Import KF` está ligado;
- se a pasta `Animations` está correta;
- se existe um `.kf` com o mesmo nome do `.nif`.

Exemplo:

```text
M001.nif
M001.kf
```

Se o `.kf` tiver outro nome, importe manualmente pelo menu `File > Import > NetImmerse/Gamebryo (.kf)`.

### O modelo veio sem textura

Confira:

- se `Use Textures` está ligado;
- se a pasta `Textures` foi selecionada;
- se as texturas realmente existem nessa pasta;
- se o Blender consegue abrir o formato `.dds` usado pelo jogo.

Alguns jogos usam caminhos internos diferentes dentro do `.nif`. Esta build tenta resolver os casos mais comuns, mas nem todos os jogos seguem o mesmo padrão.

### Erro "StructRNA of type ... has been removed"

Esta build inclui correções para reduzir esse erro durante ativação, desativação e uso dos operadores. Se ainda acontecer:

1. Desative o addon.
2. Feche o Blender.
3. Abra o Blender novamente.
4. Ative o addon.

Se persistir, abra uma issue com o traceback completo.

## Limites conhecidos

- Esta é uma build experimental.
- Nem todos os formatos `.nif` de todos os jogos foram testados.
- A lógica principal de import/export ainda é a do addon NifTools original.
- O helper Aura Kingdom ainda não gera preview visual de modelos.
- A conversão `.dds` para `.png` só converte imagens já carregadas no Blender.
- Algumas texturas `.dds` podem não abrir dependendo do formato/compressão.

## Dicas para abrir issue

Ao reportar um problema, inclua:

- versão exata do Blender;
- nome do jogo;
- tipo de arquivo (`.nif`, `.kf`, `.dds`);
- print ou texto completo do erro;
- se usou import normal ou o Aurakingdom Helper;
- estrutura das pastas usadas.

Exemplo de estrutura útil:

```text
model/M001.nif
animation/M001.kf
texture/M001.dds
```

## Créditos e licença

Este projeto é baseado no trabalho original do **NifTools Team**.

Projeto original:

```text
https://github.com/niftools/blender_niftools_addon
```

Documentação original:

```text
https://blender-niftools-addon.readthedocs.io/
```

Esta build preserva a base, créditos e licença do projeto original. Veja `LICENSE.rst`, `AUTHORS.rst` e os arquivos de licença incluídos no repositório.

## Aviso importante

Esta build não é oficial, não substitui o projeto NifTools original e pode ter comportamentos inesperados em arquivos de jogos diferentes.

Sempre mantenha backup dos seus `.blend`, `.nif`, `.kf` e texturas antes de importar, editar ou exportar.
