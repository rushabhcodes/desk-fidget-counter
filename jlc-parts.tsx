// Exact JLCPCB/EasyEDA imports; generated files remain unchanged.
import { RP2040 } from "./imports/jlc/RP2040"
import { W25Q16JVSNIQ } from "./imports/jlc/W25Q16JVSNIQ"
import { ABM8_272_T3 } from "./imports/jlc/ABM8_272_T3"
import { A_0402CG150J500NT } from "./imports/jlc/A_0402CG150J500NT"
import { A_0603WAF270JT5E } from "./imports/jlc/A_0603WAF270JT5E"
import { A_0603WAF1001T5E } from "./imports/jlc/A_0603WAF1001T5E"

import { Children, cloneElement, createElement, isValidElement } from "react"
import { MB85RC256VPNF_G_AMERE2 } from "./imports/jlc/MB85RC256VPNF_G_AMERE2"
import { GRM188R61A105KA61D } from "./imports/jlc/GRM188R61A105KA61D"
import { CL21A475KOFNNNE } from "./imports/jlc/CL21A475KOFNNNE"
import { GRM188R71C104KA01D } from "./imports/jlc/GRM188R71C104KA01D"
import { GRM155R71C104KA88D } from "./imports/jlc/GRM155R71C104KA88D"
import { GRM155R71H103KA88D } from "./imports/jlc/GRM155R71H103KA88D"
import { TYPEC_309_ACP16L65 } from "./imports/jlc/TYPEC_309_ACP16L65/TYPEC_309_ACP16L65"
import { B6B_PH_K_S_LF__SN_ } from "./imports/jlc/B6B_PH_K_S_LF__SN_"
import { RC0603FR_0710KL } from "./imports/jlc/RC0603FR_0710KL"
import { RC0603FR_075K1L } from "./imports/jlc/RC0603FR_075K1L"
import { RC0603FR_074K7L } from "./imports/jlc/RC0603FR_074K7L"
import { RC0603FR_07100KL } from "./imports/jlc/RC0603FR_07100KL"
import { RC0603FR_07150RL } from "./imports/jlc/RC0603FR_07150RL"
import { RC0603FR_0722KL } from "./imports/jlc/RC0603FR_0722KL"
import { RC0603FR_0722RL } from "./imports/jlc/RC0603FR_0722RL"
import { B3U_3000P } from "./imports/jlc/B3U_3000P"
import { TPS22919DCKR } from "./imports/jlc/TPS22919DCKR"
import { TLV75533PDBVR } from "./imports/jlc/TLV75533PDBVR"
import { STM32F072CBT6 } from "./imports/jlc/STM32F072CBT6"
import { USBLC6_2SC6 } from "./imports/jlc/USBLC6_2SC6"
import { SN74LVC2G17DBVR } from "./imports/jlc/SN74LVC2G17DBVR"
import { TCUT1600X01 } from "./imports/jlc/TCUT1600X01"
import { A_2_54_1_8 } from "./imports/jlc/A_2_54_1_8"
import { A_61300821021 } from "./imports/jlc/A_61300821021/A_61300821021"
import { SM08B_SRSS_TB_LF__SN_ } from "./imports/jlc/SM08B_SRSS_TB_LF__SN_/SM08B_SRSS_TB_LF__SN_"
export const jlcParts: Record<string, (props: any) => any> = {
  "RP2040": RP2040,
  "W25Q16JVSNIQ": W25Q16JVSNIQ,
  "ABM8-272-T3": ABM8_272_T3,
  "0402CG150J500NT": A_0402CG150J500NT,
  "0603WAF270JT5E": A_0603WAF270JT5E,
  "0603WAF1001T5E": A_0603WAF1001T5E,

  "MB85RC256VPNF-G-AMERE2": MB85RC256VPNF_G_AMERE2,
  "GRM188R61A105KA61D": GRM188R61A105KA61D,
  "CL21A475KOFNNNE": CL21A475KOFNNNE,
  "GRM188R71C104KA01D": GRM188R71C104KA01D,
  "GRM155R71C104KA88D": GRM155R71C104KA88D,
  "GRM155R71H103KA88D": GRM155R71H103KA88D,
  "TYPEC-309-ACP16L65": TYPEC_309_ACP16L65,
  "B6B-PH-K-S(LF)(SN)": B6B_PH_K_S_LF__SN_,
  "RC0603FR-0710KL": RC0603FR_0710KL,
  "RC0603FR-075K1L": RC0603FR_075K1L,
  "RC0603FR-074K7L": RC0603FR_074K7L,
  "RC0603FR-07100KL": RC0603FR_07100KL,
  "RC0603FR-07150RL": RC0603FR_07150RL,
  "RC0603FR-0722KL": RC0603FR_0722KL,
  "RC0603FR-0722RL": RC0603FR_0722RL,
  "B3U-3000P": B3U_3000P,
  "TPS22919DCKR": TPS22919DCKR,
  "TLV75533PDBVR": TLV75533PDBVR,
  "STM32F072CBT6": STM32F072CBT6,
  "USBLC6-2SC6": USBLC6_2SC6,
  "SN74LVC2G17DBVR": SN74LVC2G17DBVR,
  "TCUT1600X01": TCUT1600X01,
  "2.54-1*8": A_2_54_1_8,
  "61300821021": A_61300821021,
  "SM08B-SRSS-TB(LF)(SN)": SM08B_SRSS_TB_LF__SN_,
}
export function jlcFootprintPart(mpn: string, props: any) {
  if ("footprint" in props) throw new Error(`Do not override the imported footprint for ${mpn}`)
  const Component = jlcParts[mpn]
  if (!Component) throw new Error(`Missing exact JLCPCB footprint for ${mpn}`)
  let imported = Component(props)
  // These housings overhang the board/window, or are DNP. Keep the supplier
  // copper, drills and courtyards; omit body ink that cannot be printed.
  // Tightly spaced resistor pairs and local bulk capacitors need one outline omitted.
  if (["TYPEC-309-ACP16L65", "B6B-PH-K-S(LF)(SN)", "2.54-1*8", "61300821021", "B3U-3000P"].includes(mpn) || ["R13", "R27", "C7", "C8", "C9", "C10", "C11", "C12", "C13", "C17", "C18", "C19", "C20", "C21", "C22", "C23", "C24"].includes(props.name)) {
    const footprint = imported.props.footprint
    const children = Children.toArray(footprint.props.children).filter(child =>
      !isValidElement(child) || !["silkscreenpath", "silkscreenrect", "silkscreencircle"].includes(String(child.type)))
    imported = cloneElement(imported, {footprint:cloneElement(footprint, {}, children)})
  }
  if (["B6B-PH-K-S(LF)(SN)", "2.54-1*8", "61300821021", "SM08B-SRSS-TB(LF)(SN)"].includes(mpn)) {
    // Access metadata only; supplier copper and drills are unchanged.
    return createElement("connector", {...imported.props,
      pinAttributes: Object.fromEntries(Array.from({length:mpn==="B6B-PH-K-S(LF)(SN)"?6:mpn==="SM08B-SRSS-TB(LF)(SN)"?10:8},(_,i)=>[`pin${i+1}`,{isPassive:true}])),
      footprint: cloneElement(imported.props.footprint, {insertionDirection:"from_above"})})
  }
  return imported
}
