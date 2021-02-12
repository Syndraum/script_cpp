> :warning: **Important note: still in development. Some bugs may appear**

## Presentation

Two actions as possible

`class.py className [...]` create .cpp and .hpp files. You can specify as many class names as you want. Class are canonical

-I option create interface

-p prefix fileName with "Class" ex : `ClassPersonnage.hpp`

-s suffix filename with ".class" ex : `Personnage.class.hpp` 

`class.sh className [...]` same as `class.py` but in shell. No option available

`update.py [...]` check .cpp and .hpp files in actual dir and generate only necessary setter and getter. You can specify class name in arguments for specific application.

`getSet.sh [...]` same as `update.py` but in shell :warning: this function do not check duplicate setter and getter

## Utilisation

run command with bash `bash ./class.sh`
or python3 `python3 ./class.py`

1. Create class

```
python3 ./class.py Personnage
```

That will create 2 files, Personnage.hpp
```cpp
#include "Personnage.hpp"

Personnage::Personnage(void){}

Personnage::Personnage(Personnage const & src)
{
	*this = src;
}

Personnage::~Personnage(void)
{
	
}

Personnage &	Personnage::operator=(Personnage const & rhs)
{
	return *this;
}
```
and Personnage.cpp
```cpp
#ifndef PERSONNAGE
# define PERSONNAGE

class Personnage
{
public:

	Personnage(void);
	Personnage(Personnage const & src);
	~Personnage(void);
	Personnage &	operator=(Personnage const &rhs);

private:

};

#endif

```

2. Insert attributes you want
```cpp
class Personnage
{
	int mana;
public:

	int life;

	Personnage(void);
	Personnage(Personnage const & src);
	~Personnage(void);
	Personnage &	operator=(Personnage const &rhs);

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
class Personnage
{
	int mana;
public:

	int life;

	Personnage(void);
	Personnage(Personnage const & src);
	~Personnage(void);
	Personnage &	operator=(Personnage const &rhs);

	int	getMana(void) const;
	int	setMana(int Mana);
	char	*getName(void) const;
	int	setName(char *Name);

private:
	char *name;
};
```
```cpp
int		Personnage::getMana(void) const
{
	return this->mana;
}

int		Personnage::setMana(int Mana)
{
	this->mana = Mana;
	return 0;
}

char	*Personnage::getName(void) const
{
	return this->name;
}

int		Personnage::setName(char *Name)
{
	this->name = Name;
	return 0;
}
```
