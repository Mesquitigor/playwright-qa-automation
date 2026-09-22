import { test, expect } from '@playwright/test';
import { camelCase } from '../src/camelCase';

test.describe('camelCase', () => {
  test('converts mixed words and hyphens from the problem statement', () => {
    expect(camelCase('BOB loves-coding')).toBe('bobLovesCoding');
  });

  test('converts delimiters *, -, and spaces', () => {
    expect(camelCase('cats AND*Dogs-are Awesome')).toBe('catsAndDogsAreAwesome');
  });

  test('converts the screenshot example without a space before Awesome', () => {
    expect(camelCase('cats AND*Dogs-areAwesome')).toBe('catsAndDogsAreawesome');
  });

  test('capitalizes single-letter words after the first', () => {
    expect(camelCase('a b c d-e-f%g')).toBe('aBCDEFG');
  });

  test('ignores consecutive and surrounding delimiters', () => {
    expect(camelCase('--hello**world!!')).toBe('helloWorld');
    expect(camelCase('  already camel? ')).toBe('alreadyCamel');
  });

  test('returns an empty string when there are no letters', () => {
    expect(camelCase('***')).toBe('');
    expect(camelCase('')).toBe('');
  });
});
