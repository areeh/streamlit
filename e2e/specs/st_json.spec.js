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

describe("st.json", () => {
  before(() => {
    cy.loadApp("http://localhost:3000/");
  });

  it("displays expanded json", () => {
    cy.getIndexed("[data-testid='stJson']", 0)
      .should("contain", "foo")
      .and("contain", "bar");
  });

  it("displays collapsed json", () => {
    cy.getIndexed("[data-testid='stJson']", 1).should("contain", "...");
  });
});
