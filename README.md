> :warning: **Important note: still in development. Some bugs may appear**

## Overview

- [Generate](#generate)
- [Update](#update)
- [Usage](#usage)

## Generate

`class.py className [...]` create .cpp and .hpp files. You can specify as many class names as you want. Class are canonical

-I option create interface

-p prefix fileName with "Class" ex : `ClassWarrior.hpp`

-s suffix filename with ".class" ex : `Warrior.class.hpp` 

`class.sh className [...]` same as `class.py` but with no option available

## Update

`update.py [...]` check all .cpp and .hpp files in actual directory and generate only necessary setter and getter. You can specify class name in arguments for specific class.

`getSet.sh [...]` same as `update.py` but in shell :warning: this function do not check duplicate setter and getter

## Usage

run command with bash `bash ./class.sh`
or python3 `python3 ./class.py`

1. Create class

```
python3 ./class.py Warrior
```

That will create 2 files, Warrior.cpp
```cpp
#include "Warrior.hpp"

Warrior::Warrior(void){}

Warrior::Warrior(Warrior const & src)
{
	*this = src;
}

Warrior::~Warrior(void)
{
	
}

Warrior &	Warrior::operator=(Warrior const & rhs)
{
	return *this;
}
```
and Warrior.hpp
```cpp
#ifndef WARRIOR
# define WARRIOR

class Warrior
{
public:

	Warrior(void);
	Warrior(Warrior const & src);
	~Warrior(void);
	Warrior &	operator=(Warrior const &rhs);

private:

};

#endif

```

2. Insert attributes you want
```cpp
class Warrior
{
	int mana;
public:

	int life;

	Warrior(void);
	Warrior(Warrior const & src);
	~Warrior(void);
	Warrior &	operator=(Warrior const &rhs);

private:
	char *name;
};
```
> :warning: Only privates attributes will be considered

3. launch update
```
python3 ./update.py
```
4. Look at the results
```cpp
class Warrior
{
	int mana;
public:

	int life;

	Warrior(void);
	Warrior(Warrior const & src);
	~Warrior(void);
	Warrior &	operator=(Warrior const &rhs);

	int	getMana(void) const;
	int	setMana(int Mana);
	char	*getName(void) const;
	int	setName(char *Name);

private:
	char *name;
};
```
```cpp
int		Warrior::getMana(void) const
{
	return this->mana;
}

int		Warrior::setMana(int Mana)
{
	this->mana = Mana;
	return 0;
}

char	*Warrior::getName(void) const
{
	return this->name;
}

int		Warrior::setName(char *Name)
{
	this->name = Name;
	return 0;
}
```
