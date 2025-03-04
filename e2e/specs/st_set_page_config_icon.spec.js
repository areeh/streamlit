/**
 * @license
 * Copyright 2018-2022 Streamlit Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

describe("st.set_page_config", () => {
  before(() => {
    cy.loadApp("http://localhost:3000/");
  });

  it("sets the page favicon with ico file", () => {
    cy.get("link[rel='shortcut icon']")
      .should("have.attr", "href")
      .should(
        "contain",
        "92018b2805266c4cb9a98e90c849ce5b5e7ba6d1af423bd7b7c345da.png"
      );
  });
});
