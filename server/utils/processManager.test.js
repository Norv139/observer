// import {describe, expect, test} from '@jest/globals';
const { ProcessManager } = require("./processManager");
const { DateTime } = require("luxon");

const pm = new ProcessManager(true);
const statusGL = [
  {
    code: null,
    discription: "",
    id: 1,
    name: "test_1",
    process: null,
    start: DateTime.now().toFormat("yyyy-MM-dd HH:mm:ss"),
    status: "run",
    token: "hide",
  },
  {
    code: null,
    discription: "",
    id: 2,
    name: "test_2",
    process: null,
    start: DateTime.now().toFormat("yyyy-MM-dd HH:mm:ss"),
    status: "run",
    token: "hide",
  },
  {
    code: null,
    discription: "",
    id: 3,
    name: "test_3",
    process: null,
    start: DateTime.now().toFormat("yyyy-MM-dd HH:mm:ss"),
    status: "run",
    token: "hide",
  },
];

test("crtBot", () => {
  expect(pm.crtBot("123", "test_1").id).toBe(1);
  expect(pm.crtBot("234", "test_2").id).toBe(2);
  expect(pm.crtBot("345", "test_3").id).toBe(3);
  expect(pm.crtBot("345", "test_4").id).toBe(undefined);
});

test("status", () => {
  expect(pm.status()).toEqual(statusGL);
});

test("killProcessById", () => {
  pm.killProcessById(1);
  expect(pm.status()).toEqual(
    statusGL.filter((item) => !["test_1", "test_4"].includes(item.name))
  );

  pm.killProcessById(3);
  expect(pm.status()).toEqual(
    statusGL.filter(
      (item) => !["test_1", "test_3", "test_4"].includes(item.name)
    )
  );

  pm.killProcessById(2);
  expect(pm.status()).toEqual([]);
});

test("Complex logic kill process By Id & By Name", () => {
  pm.crtBot("1", "test_1");
  pm.crtBot("2", "test_2");
  pm.crtBot("3", "test_3");

  pm.killProcessById(1);
  pm.killProcessByName("test_2");

  pm.crtBot("4", "test_4");

  expect(pm.status().map((item) => item.name)).toEqual(["test_3", "test_4"]);

  pm.killProcessById(3);
  pm.killProcessById(4);

  expect(pm.status()).toEqual([]);

  pm.crtBot("1", "test_1");
  pm.crtBot("2", "test_2");

  expect(pm.killProcessByName("test")).toEqual([
    { id: 1, name: "test_1" },
    { id: 2, name: "test_2" },
  ]);
});
